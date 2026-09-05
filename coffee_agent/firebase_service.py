import firebase_admin
from firebase_admin import firestore

# Initialize Firebase only once
if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()


def save_chat(user_id: str, user_message: str, assistant_message: str):
    """
    Save a chat message under the authenticated user's Firestore path.
    """
    chat_ref = db.collection("users").document(user_id).collection("chats").document()

    chat_ref.set({
        "user_message": user_message,
        "assistant_message": assistant_message,
    })

    return chat_ref.id
