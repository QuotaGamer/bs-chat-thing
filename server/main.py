from typing import Any
from flask import request, jsonify, Flask
from funcs import register_user, login_user, message as messag, create_converastion, verify_token
from flask_socketio import SocketIO, emit, disconnect
from os.path import exists as path_exist
from os import urandom as rand, chmod as mod
from typing import Union
from datetime import datetime
import json
def getkey() -> bytes:
    if path_exist("./secret"):
        with open("./secret", "rb") as f:
            key = f.read()
    else:
        with open("./secret", "wb") as f:
            key = rand(24)
            f.write(key)
            mod("./secret", 0o600)
    return key
SECRET_KEY = getkey()
sessions:dict[str, Any] = {}
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/register', methods=['POST'])
def register():
    data:dict[str, str] = request.json
    username = data.get('username')
    password = data.get('password')
    token = register_user(username, password, SECRET_KEY)
    if token:
        return jsonify({"token": token}), 201
    else:
        return jsonify({"message": "Username already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data:dict[str, str] = request.json
    username = data.get('username')
    password = data.get('password')
    token = login_user(username, password)
    if token:
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# socket stuff

@socketio.on('message')
def handle_message(msg:str) -> None:
    try:
        data:dict[str, Union[list, str, dict, int, float, None]] = json.loads(msg)
    except Exception as e:
        print(f"[LOG] {e} caught (not JSON?)")
        emit('response', {'error': 'Content must be proper JSON.'})
    else:
        opcode = data.get("op")
        if opcode == 0: # login code
            token = data.get("token")
            if token:
                user = verify_token(token)
                if user:
                    sessions.update({request.sid: token})
                    emit('response', {'username': user['username']})
                    return None
                else:
                    emit('response', {'error': 'Invalid token.'})
                    disconnect()
                    return None
            else:
                emit('response', {'error': 'No token provided.'})
                disconnect()
                return None
        elif opcode == 1: # send message
            if sessions.get(request.sid):
                if data.get("conversation"):
                    if data.get("content"):
                        _msg = messag(conversation=data.get("conversation"), token=sessions.get(request.sid), content=data.get("content"), key=SECRET_KEY)
                        if _msg:
                            emit('response', _msg)
                        else:
                            emit('response', {'error': 'Unlogged error, check debug log.'})
                    else:
                        emit('response', {'error': 'You must provide message content to send messages.'})
                else:
                    emit('response', {'error': 'You must provide a conversation for sending messages.'})
        elif opcode == 2: # receive message, server only
            emit('response', {'error': 'Server only. You (as a client) should not be sending this.'})

# end socket stuff

@app.route('/message', methods=['POST'])
def message():
    data:dict[str, str] = request.json
    id = data.get('id')
    token = data.get('token')
    content = data.get('content')
    if not id:
        return jsonify({"message": "Invalid conversation."}), 401
    elif not content:
        return jsonify({"message": "You cannot send an empty message."}), 401
    else:
        msg = messag(id, token, content, SECRET_KEY)
        if msg:
            return jsonify(msg), 200
        else:
            return jsonify({"message": "Invalid token."}), 401

@app.route("/new-conversation", methods=['POST'])
def addconv():
    data:dict[str, str] = request.json
    token:str = data.get('token')
    members:list[str] = data.get('members')
    title:str|None = data.get('title')
    print(token, members, title)
    conv = create_converastion(members, title if title else "Unnamed", token, SECRET_KEY)
    if conv:
        return jsonify(conv), 200
    else:
        return jsonify({"message": "Invalid token."}), 401
    """THIS feels WAY TOO EASY"""
    """I swear it isn't done, yet it looks like it is.."""
    """I think I'm going insane."""
app.run()
socketio.run(app=app, host="0.0.0.0", port=39472, debug=True)