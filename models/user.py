from firebase_set import db
from datetime import datetime

class UserModel:
    def __init__(self, id: str, name: str, email: str, created_at: datetime):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = created_at

    @staticmethod
    def from_firestore(doc):
        data = doc.to_dict()
        return UserModel(
            id=doc.id,
            name=data.get('name'),
            email=data.get('email'),
            created_at=data.get('created_at')
        )

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at
        }

    def save(self):
        doc_ref = db.collection('users').document(self.id)
        doc_ref.set(self.to_dict())

    @staticmethod
    def get(user_id: str):
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return UserModel.from_firestore(doc)
        else:
            raise ValueError('User not found')

    def get_user(db, id: str):
     if id in db:
        return UserModel(**db[id])
    