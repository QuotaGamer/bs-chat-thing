import os
def getkey() -> bytes:
    if os.path.exists("./secret"):
        with open("./secret", "rb") as f:
            key = f.read()
    else:
        with open("./secret", "wb") as f:
            key = os.urandom(24)
            f.write(key)
            os.chmod("./secret", 0o600)
    return key
SECRET_KEY = getkey()
from flask import request, jsonify, Flask
from funcs import register_user, login_user, message as messag, create_converastion
app = Flask(__name__)

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
    token = login_user(username, password, SECRET_KEY)
    if token:
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

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

app.run("0.0.0.0", 39472, True, False)