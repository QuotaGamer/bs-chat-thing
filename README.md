# bs-chat-app

A basic (and arguably crappy) chat server built with Flask. This app provides a simple backend to handle user registration, login, and messaging functionality. The app includes a few endpoints for interaction and a basic client example script.

## Endpoints

### 1. `/message` (POST)
Sends a message to an existing conversation.

**Request body (JSON)**:
```json
{
  "id": "string",               // The ID of the conversation
  "token": "string",            // User's token for authentication
  "content": "string"           // The message content
}
```

**Response (JSON)**:
```json
{
  "random-id": {               // Message ID
    "user": "string",          // Your username
    "content": "string"        // The content you specified
  }
}
```

### 2. `/new-conversation` (POST)

Creates a new conversation with a random ID.

**Request body (JSON)**:
```json
{
  "token": "string",             // User's token for authentication
  "members": ["user1", "user2"], // List of members for the conversation (Can be only one person)
  "title": "string"              // The title of the conversation
}
```

**Response (JSON)**:
```json
{
  "conversation_id": "random-id",   // ID of the newly created conversation
  "title": "string",                // The title of the conversation
  "members": ["user1", "user2"]     // List of members in the conversation
}
```

### 3. `/login` (POST)

Logs into a premade account and returns a token.

**Request body (JSON)**:
```json
{
  "username": "string",             // Username of the user
  "password": "string"              // Password of the user
}
```

**Response (JSON)**:
```json
{
  "token": "string"                 // The authentication token for the user
}
```

### 4. `/register` (POST)

Registers a new account and returns a token.

**Request body (JSON)**:
```json
{
  "username": "string",           // Desired username
  "password": "string"            // Desired password
}
```

**Response (JSON)**:
```json
{
  "token": "string"               // The authentication token for the new user
}
```

## Client Example

A Python script is included as an example "client" for interacting with the server. You can use it to register, log in, create conversations, and send messages.

### Requirements

- Python 3.10+ (required for f-strings)
- Flask (pip install Flask)

## Running the Server

To start the Flask server, run the following command in the `server` folder:

```bash
python main.py
```

By default, the server will run on `http://0.0.0.0:39472/`.

## License

There's no license (yet), I don't care what you do as long as you credit me, don't turn it into malware, and don't sell it.
