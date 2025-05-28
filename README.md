# Text Saver Microservice

This microservice allows clients to save and retrieve user-specific text. It communicates over a **ZeroMQ socket** and stores data in **Google Firestore** using the Firebase Admin SDK.

---

## First-Time Setup Instructions

Follow these steps to run the microservice for the first time.

### 1. Install Required Python Packages

```bash
pip install pyzmq firebase-admin
```

### 2. Setup Firebase Admin SDK

1. Go to the Firebase Console.
2. Create a project (or use an existing one).
3. Navigate to:
`Project Settings > Service Accounts > Generate new private key`
4. Download the .json key file and save it in your project folder (e.g., serviceAccountKey.json).

### 3. Save the Server Code

Save the server code in your repository found in `text_saver_server.py`. This completes the setup.


## Microservice Address

- Protocol: `ZeroMQ REP`
- Address: `tcp://localhost:5555`

---

## How to PROGRAMMATICALLY REQUEST Data

To request data, send a **JSON message** over a ZeroMQ socket using the `REQ` pattern.

### Request Parameters

| Parameter  | Type     | Required | Description                                   |
|------------|----------|----------|-----------------------------------------------|
| `user_id`  | `string` | Yes      | The unique ID of the user                     |
| `action`   | `string` | Yes      | One of `"save"` or `"history"`                |
| `words`    | `list`   | No       | List of strings to save (used with `save`)    |

---

### Example Request (Python)

```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

request = {
    "user_id": "user_123",
    "action": "save",
    "words": ["integration", "curve", "multi-language"]
}

socket.send_json(request)
response = socket.recv_string()
print("Server response:", response)
```

---

### UML Diagram

![microserviceAUMLDiagram](https://github.com/user-attachments/assets/45a99c80-9b7b-4ecd-94ee-ec86f22a72e5)
