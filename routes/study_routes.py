from fastapi import APIRouter, HTTPException, Depends
from schemas.schemas import UserSchema, Token
import requests
import os
from firebase_set import auth, db

router = APIRouter()

# Firebase API 키가 설정되어 있는지 확인
FIREBASE_API = os.getenv('FIREBASE_API')
if FIREBASE_API is None:
    raise ValueError("FIREBASE_API environment variable is not set")

@router.post("/create")
async def create_new_user(create_user: UserSchema):
    try:
        # 이메일과 비밀번호 필드가 있는지 확인
        if not create_user.email or not create_user.password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        user_data = {
            "email": create_user.email,
            "name": create_user.name,
            "phone": create_user.phone,
            "created_at": create_user.created_at,
        }

        # Firebase에서 사용자 생성
        user_record = auth.create_user(
            email=create_user.email,
            password=create_user.password,
            display_name=create_user.name,
            phone_number=create_user.phone,
            disabled=False,
        )

        # Firestore에 사용자 데이터 저장
        db.collection('users').document(user_record.uid).set(user_data)
        return {"message": "User created successfully", "user_data": user_data}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(data: UserSchema):
    try:
        firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API}"
        payload = {
            "email": data.email,
            "password": data.password,
            "returnSecureToken": True
        }
        response = requests.post(firebase_url, json=payload)

        # Firebase 응답 처리
        response_data = response.json()
        if response.status_code != 200:
            error_message = response_data.get('error', {}).get('message', 'Invalid email or password')
            raise HTTPException(status_code=400, detail=error_message)

        # idToken이 응답에 포함되어 있는지 확인
        if 'idToken' not in response_data:
            raise HTTPException(status_code=400, detail="Unable to retrieve idToken from Firebase")

        id_token = response_data['idToken']
        return Token(access_token=id_token, token_type="Bearer")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
