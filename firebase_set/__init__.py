import firebase_admin
from firebase_admin import credentials, auth, firestore
from config.config import settings

def initialize_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_JSON)
            firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        raise

initialize_firebase()

__all__ = ["auth", "firestore"]
