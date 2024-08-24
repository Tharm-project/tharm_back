import firebase_admin
from firebase_admin import auth, firestore, storage

firebase_admin.initialize_app()
db = firestore.client()
bucket = storage.bucket()

__all__ = ["auth", "firestore"]
