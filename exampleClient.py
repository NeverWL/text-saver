import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Save request
save_request = {
    "user_id": "user_123",
    "action": "save",
    "words": ["Latest", "is", "this!"]
}
socket.send_json(save_request)
print("Server response:", socket.recv_string())

# History request
socket.send_json({
    "user_id": "user_123",
    "action": "history"
})
print("History:", socket.recv_json())

# Get Latest request
socket.send_json({
    "user_id": "user_123",
    "action": "latest"
})
response = socket.recv_json()
print("Latest saved entry:", response)
