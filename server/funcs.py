import jwt, datetime, hashlib, random, json_helper, logging
log = logging.Logger(__name__)
usermgr = json_helper.JSONManager("./users.json")
msgmgr = json_helper.JSONManager("./conversations.json")
def generate_token(username:str, SECRET_KEY:str|bytes):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    token = jwt.encode({'username': username, 'exp': expiration}, SECRET_KEY, algorithm="HS256")
    return token

def register_user(username:str, password:str, key:str|bytes):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    token = generate_token(username, key)
    
    if not usermgr.get_key(username, default=False):
        log.debug(f"User @{username} created.")
        usermgr.update_data(username, [hashed_password, token, []])
        return token
    else:
        return None

def update_token_in_db(username:str, new_token:str):
    data:list[str, str] = usermgr.get_key(username)
    log.debug(f"User @{username} generated new token.")
    usermgr.update_data(username, [data[0], new_token])

def login_user(username:str, password:str, key:str|bytes):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user:None|list[str, str] = usermgr.get_key(username, default=None)
    if user:
        if hashed_password == user[0]:
            log.debug(f"User @{username} logged in.")
            return user[1]
        else:
            log.debug(f"Someone tried to login as @{username} and failed from invalid redentials.")
            return None
    else:
        log.debug(f"Someone tried to login as @{username}, but the user doesn't exist.")
        return None

def verify_token(token:str, SECRET_KEY:str|bytes) -> dict[str, str|datetime.datetime] | None:
    try:
        payload:dict[str, str|datetime.datetime] = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        log.debug("Token check passed.")
        return payload
    except jwt.ExpiredSignatureError:
        log.warning("Token check failed (Expired)")
        return None
    except jwt.InvalidTokenError:
        log.warning("Token check failed (Invalid)")
        return None

def get_conversation(id:str) -> dict[str, str] | None:
    conv = msgmgr.get_key(id)
    if conv:
        return conv
    else:
        return None

def message(conversation: str, token: str, content: str, key: str|bytes) -> dict[str, str] | None:
    conv: dict[str, str|dict[str, str]] = msgmgr.get_key(conversation)
    if conv:
        user = verify_token(token, key)["username"]
        _user = usermgr.get_key(user)
        if conversation in _user[2]:
            if len(content) <= 4000:
                id = generate_id()
                conv["messages"].update({id: { "user": user, "content": content }})
                msgmgr.update_data(conversation, conv)
                return {id: { "user": user, "content": content }}
            else:
                log.warning(f"Message from @{user} was too long!")
                return None
        else:
            log.warning("User tried to message conversation they couldn't access.")
            return None

def get_converastions(token: str, key: str|bytes) -> list:
    tuser = verify_token(token, key)
    if tuser:
        user:list[str, str, dict[str, str]] = usermgr.get_key(tuser["username"])
        return user[2]
    else:
        return None

def add_conversation_to_user(user: str, id: str) -> None:
    _user:list[str, str, list[str]] = usermgr.get_key(user)
    _user[2].append(id)
    usermgr.update_data(user, _user)
    return None
    """This feels WAY too simple."""

def create_converastion(members: list[str], title:str, token:str, key:str|bytes) -> str:
    user = verify_token(token, key)
    if user:
        id = generate_id()
        for member in members:
            add_conversation_to_user(member, id)
        msgmgr.update_data(id, {"messages": {}, "title": title})
        return {"id": id, "members": members}
    else:
        return None

def generate_id() -> str:
    log.debug("Generated new conversation ID")
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])