import zmq
import json

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
            "words": words
        })
        socket.send_string("Save successful.")
    elif action == "history":
        docs = db.collection("expressions").document(user_id).collection("entries").stream()
        history = [doc.to_dict() for doc in docs]
        socket.send_json(history)
    else:
        socket.send_string("Invalid request.")
