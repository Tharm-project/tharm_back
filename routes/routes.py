from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from models.user import User

# 라우터 생성
router = APIRouter()

# db 연결
db = firestore.client()

# 여기에 api를 작성하시면 됩니다!!
@router.post("/users/")
def create_user(user: User):
    doc_ref = db.collection("users").document(user.id)
    doc_ref.set(user.dict())
    return {"message": "User created successfully"}

@router.get("/users/{user_id}")
def get_user(user_id: str):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="User not found")