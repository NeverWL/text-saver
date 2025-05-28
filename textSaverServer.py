import zmq
import json
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('multiliingual-text-extractor-firebase-adminsdk-fbsvc-f8524228f6.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

print("Successfully connected to Firestore!")

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Server started. Waiting for requests...")

while True:
    request = socket.recv_json()

    user_id = request.get("user_id")
    action = request.get("action")  # either "save" or "history"
    words = request.get("words", [])

    if action == "save" and words:
        doc_ref = db.collection("expressions").document(user_id).collection("entries").document()        
        doc_ref.set({
            "words": words,
            "timestamp": datetime.now(timezone.utc)
        })
        socket.send_string("Save successful.")
    elif action == "history":
        docs = db.collection("expressions").document(user_id).collection("entries").stream()
        history = []
        for doc in docs:
            data = doc.to_dict()
            if "timestamp" in data:
                data["timestamp"] = data["timestamp"].isoformat()
            history.append(data)
        socket.send_json(history)
    elif action == "latest":
        docs = db.collection("expressions").document(user_id).collection("entries") \
                .order_by("timestamp", direction=firestore.Query.DESCENDING) \
                .limit(1) \
                .stream()
        
        latest = next(docs, None)
        if latest:
            data = latest.to_dict()
            if "timestamp" in data:
                data["timestamp"] = data["timestamp"].isoformat()
            socket.send_json(data)
        else:
            socket.send_json({"message": "No saved entries found."})
    else:
        socket.send_string("Invalid request.")
