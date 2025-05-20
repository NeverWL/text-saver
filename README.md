# Multilingual Text Saver Microservice

This microservice allows clients to save and retrieve user-specific lists of words extracted from images. It communicates over a **ZeroMQ socket** and stores data in **Google Firestore** using the Firebase Admin SDK.

---

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
![image](https://github.com/user-attachments/assets/8c69734e-0a21-44ff-9f8a-37c37faa1b1c)
