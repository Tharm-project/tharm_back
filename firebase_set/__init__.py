import firebase_admin

from firebase_admin import credentials, auth, db

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("/firebase_set/tharm-16f63-firebase-adminsdk-ir9sb-fc5140cab4.json")
        default_app = firebase_admin.initialize_app(cred)
        print(default_app.name)

def get_db(path = 'items'):
    return db.reference(path)