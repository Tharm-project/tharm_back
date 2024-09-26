from fastapi import APIRouter, HTTPException, Depends
from schemas.schemas import UserSchema, Token, UserSearchSchema, PasswordResetSchema, loginSchema
from firebase_admin import auth as firebase_auth
import requests
from firebase_set import auth, db
from services.emailutils import send_reset_email
from datetime import datetime, timezone


router = APIRouter()

@router.post("/create")
async def create_new_user(create_user: UserSchema):
    try:
        # 이메일과 비밀번호 필드가 있는지 확인
        if not create_user.email or not create_user.password:
            raise HTTPException(status_code=400, detail="Email and password are required")
        
        # Firestore에 문서 생성
        user_ref = db.collection('user').document()

        user_data = {
            "id": user_ref.id,
            "email": create_user.email,
            "name": create_user.name,
            "phone": create_user.phone,
            "created_at": datetime.now(timezone.utc),
        }

        # Firestore에 사용자 데이터 저장
        user_ref.set(user_data)
        return {"message": "User created successfully", "user_data": user_data}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# @router.post("/login", response_model=Token)
# async def login(data: loginSchema):
#     try:
#         firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API}"
#         print(firebase_url)
#         payload = {
#             "email": data.email,
#             "password": data.password,
#             "returnSecureToken": True
#         }
#         response = requests.post(firebase_url, json=payload)

#         # Firebase 응답 처리
#         response_data = response.json()
#         if response.status_code != 200:
#             error_message = response_data.get('error', {}).get('message', 'Invalid email or password')
#             raise HTTPException(status_code=400, detail=error_message)

#         # idToken이 응답에 포함되어 있는지 확인
#         if 'idToken' not in response_data:
#             raise HTTPException(status_code=400, detail="Unable to retrieve idToken from Firebase")

#         id_token = response_data['idToken']
#         return Token(access_token=id_token, token_type="Bearer")

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# 아이디(이메일) 검색
@router.post("/find/id")
def find_user(user_info: UserSearchSchema):
    try:
        # Firestore에서 사용자 이름과 전화번호로 사용자 검색
        doc_ref = db.collection('user').where('name', '==', user_info.name).where('phone', '==', user_info.phone)

        user_docs = doc_ref.stream()

        user_data = None
        for user_doc in user_docs:
            user_data = user_doc.to_dict()
            break

        if not user_data:
            raise HTTPException(status_code=404, detail="일치하는 사용자를 찾을 수 없습니다.")

        return {"email": user_data.get('email')}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 비밀번호 재설정 요청
@router.post("/find/reset-password")
def reset_password(data: PasswordResetSchema):
    try:
        # Firebase Authentication을 사용하여 사용자 검색
        user = firebase_auth.get_user_by_email(data.email)

        if not user:
            raise HTTPException(status_code=400, detail="존재하지 않는 유저입니다.")
        
        # Firebase Authentication을 사용하여 비밀번호 재설정 링크 생성
        reset_link = firebase_auth.generate_password_reset_link(data.email)

        # 해당 링크를 포함한 이메일 발송 (send_reset_email은 가정된 유틸리티 함수)
        send_reset_email(data.email, reset_link)

        return {"message": "비밀번호 재설정 메일을 발송하였습니다."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    