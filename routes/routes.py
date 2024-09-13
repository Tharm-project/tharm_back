# from firebase_set import auth, db
# from fastapi.security import OAuth2PasswordBearer
# from schemas.schemas import UserSchema, Token
# from fastapi.encoders import jsonable_encoder
# from datetime import datetime
# from controller import study_controller
# from fastapi import FastAPI, APIRouter, HTTPException
# from services.emailutils import send_reset_email, generate_reset_pwtoken, get_email_from_pwtoken
# from itsdangerous import SignatureExpired
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# import os
# from dotenv import load_dotenv
# import requests
# from fastapi import Depends

# # .env 파일의 환경 변수를 로드
# load_dotenv()

# FIREBASE_API = os.getenv('FIREBASE_API')

# app = FastAPI()
# router = APIRouter()
# studyController = study_controller.StudyController()

# # 템플릿 디렉터리 설정
# templates = Jinja2Templates(directory="templates")

# #datetime format set
# def format_datetime(dt: datetime) -> str:
#     return dt.strftime('%Y-%m-%d %H:%M:%S')

# # 비밀번호 Hash 처리
# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# # def hash_password(password: str) -> str:
# #     return pwd_context.hash(password)

# # 비밀번호 검증
# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
# # async def get_current_user(token: str = Depends(oauth2_scheme)):
# #     try:
# #         # 토큰 검증
# #         decoded_token = auth.verify_id_token(token)
# #         user = auth.get_user(decoded_token['uid'])
# #         return user
# #     except Exception as e:
# #         raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {str(e)}")

# # 비밀번호 검증
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         # 토큰 검증
#         decoded_token = auth.verify_id_token(token)
#         user = auth.get_user(decoded_token['uid'])
#         return user
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {str(e)}")

# @router.get("/")
# def home_page():
#     # 메인 페이지(첫화면)은 현재 학습 중인 목록, 학습 목록 출력
#     try:
#         if authorization:
#             token = authorization.split(" ")[1]
#             user_ref = get_current_user(token)
#             user_doc = user_ref.get()
#             user_data = user_doc.to_dict()

#             if not user_doc.exists:
#                 raise HTTPException(status_code = 404, detail = "사용자를 찾을 수 없습니다.")
            
#             # 메인화면에 필요한 정보 넘김
#             study_ref = db.collection('study').filter('user_id','==',user_doc['uid']).order_by('created_at',direction=firestore.Query.DESCENDING).limit(1)
#             study_docs = study_ref.stream()
#             stduy_data = study_docs.to_dict()

#             # 광고 정보 넘기기
#             ads_ref = db.collection('AD')
#             ads_docs = ads_ref.stream()

#             ads_list = []

#             for doc in ads_docs:
#                 ad_data = doc.to_dict()
#                 ad_data['id'] = doc.id
#                 ads_list.append(ad_data)


#             return {"user": f"welcome {user_data.get('name')}!",
#                     "last_study": f"Last study is {stduy_data.get('name')}, and progress is {stduy_data.get('status')}",
#                     "advertisement": f"advertisement: {ads_list}"}
#         else:
#             raise HTTPException(status_code=401, detail = "로그인을 안했어요")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"홈페이지 로드 중 오류: {str(e)}")


# # 회원가입
# @router.post("/create/user")
# async def create_new_user(create_user: UserSchema):
#     try:
#         # hashed_password = hash_password(create_user.password) #해쉬처리한 비밀번호로 저장
#         # 이후 비밀번호 찾기 시엔 이메일 체크 후 비밀번호 재설정으로 넘기기
#         # 비밀번호 원본 데이터는 우리도 모르기 때문
        
#         # Firestore에 사용자 저장 (id는 Firebase Auth에서 생성된 uid로 설정)
#         user_data = {
#             "email": create_user.email,
#             "name": create_user.name,
#             "phone": create_user.phone,
#             "created_at": format_datetime(create_user.created_at) if create_user.created_at else None,
#         }

#         # Firebase Authentication에 사용자 생성 (비밀번호는 저장되지 않음)
#         user_record = auth.create_user(
#             email=create_user.email,
#             password = create_user.password,
#             display_name=create_user.name,
#             phone_number = create_user.phone,
#             disabled=False
#         )
        
#         # Firestore에 사용자의 uid를 키로 하여 데이터 저장
#         db.collection('users').document(user_record.uid).set(user_data)

#         return {"message": "회원가입 생성 완료!", "user_data": jsonable_encoder(user_data)} #추후 프론트에서 필요한 값 있는지 체크(문구 등)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # 로그인
# @router.post("/user/login", response_model=Token)
# async def login(data: UserSchema):
#     try:
#         # Firebase Authentication REST API를 통해 로그인
#         firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API}"
#         payload = {
#             "email": data.email,
#             "password": data.password,
#             "returnSecureToken": True
#         }
#         response = requests.post(firebase_url, json=payload)
#         response_data = response.json()
        
#         if response.status_code != 200:
#             raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 유효하지 않습니다.")
        
#         # ID 토큰 반환
#         id_token = response_data['idToken']

#         # ID 토큰에서 UID 추출
#         decoded_token = auth.verify_id_token(id_token)
#         uid = decoded_token['uid']

#         # Firestore에서 사용자 데이터 가져오기
#         # user_ref = db.collection('users').document(user.uid)
#         user_ref = db.collection('user').document(uid)
#         user_doc = user_ref.get()

#         if not user_doc.exists:
#             raise HTTPException(status_code=400, detail="사용자가 존재하지 않습니다.")

#         return Token(access_token= id_token, token_type = "Bearer")
    
#         # firebase Authentication을 사용하면서 자체 토큰을 사용하지 않아도 된다.
#         # user_data = user_doc.to_dict()
#         # hashed_password = user_data.get('password')  # 키 이름을 'password'로 사용

#         # 비밀번호 검증
#         # if not pwd_context.verify(data.password, hashed_password):
#         #     raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 유효하지 않습니다.")

#         # 비밀번호가 일치하면 커스텀 토큰 생성
#         # custom_token = auth.create_custom_token(user.uid)
        
#         # Token 스키마로 반환
#         # return Token(access_token=custom_token.decode('utf-8'), token_type="Bearer")
        
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# #아이디, 비밀번호 찾기
# @router.get("/find/id")
# def find_user(user_id:str):
#     try:
#         doc_ref = db.collection('user').document(user_id)
#         user_doc = doc_ref.get()

#         if not user_doc.exists:
#             raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

#         user_data = user_doc.to_dict()
#         # print(user_data)
#         return user_data

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # 비밀번호 재설정 요청
# @router.post("/find/reset-password")
# def reset_password(data: UserSchema):
#     try:
#         # Firebase Authentication을 사용하여 비밀번호 재설정 링크를 이메일로 전송
#         # Todo: 재설정 메일 테스트 필요

#         email = data.email

#         # 이메일이 유효한지 확인
#         if not auth.get_user_by_email(email):
#             raise HTTPException(status_code=400, detail="존재하지 않는 유저입니다.")
        
#         # 비밀번호용 토큰 생성
#         token = generate_reset_pwtoken(email)

#         # Firestore에 토큰 저장
#         token_data = {
#             "email": email,
#             "token": token,
#             "creaeted_at": datetime.utcnow()
#         }
#         db.collection('password_reset_tokens').document(token).set(token_data)

#         # 이메일 발송 -> 환경설정 파일에 이메일 넣어둘것
#         send_reset_email(email, token)

#         return {"message": "비밀번호 재설정 메일을 발송하였습니다."}

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # 비밀번호 링크 요청시 반환할 페이지
# @router.get("/reset-password/{token}", response_class=HTMLResponse)
# def reset_password_form(token: str):
#     try:
#         # 토큰 검증 (유효 시간 검사)
#         get_email_from_pwtoken(token)

#         # 검증된 토큰과 함께 비밀번호 재설정 폼 렌더링
#         return templates.TemplateResponse("reset_password.html")

#     except SignatureExpired:
#         raise HTTPException(status_code=400, detail="토큰이 만료되었습니다.")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"토큰 검증 중 오류가 발생했습니다: {str(e)}")

# # 비밀번호 교체 후 firestore에 업데이트
# @router.patch("/reset-password")
# def complete_reset_password(token: str = Form(...), new_password: str = Form(...)):
#     try:
#         # 토큰에서 이메일 추출
#         email = get_email_from_pwtoken(token)

#         # Firestore에서 사용자 데이터 가져오기
#         user_doc = db.collection('user').filter('email', '==', email).get()
  
#         if not user_doc:
#             raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")
        
#         # 비밀번호 해싱
#         #hashed_password = hash_password(new_password)

#         # Firestore에 해싱한 비밀번호 저장
#         user_ref = user_doc[0].reference
#         #user_ref.update({'password': hashed_password})

#         # 비밀번호 재설정 후 Firestore에서 토큰 삭제
#         db.collection('password_reset_tokens').document(token).delete()

#         return {"message": "비밀번호가 성공적으로 변경되었습니다."}
#     except SignatureExpired:
#         raise HTTPException(status_code=400, detail = "토큰이 만료되었습니다.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"비밀번호를 재설정하는 중 오류가 발생했습니다: {str(e)}")

# # # 유저 검색
# # @router.get("/users/{name}")
# # def get_user(name: str):

# #     doc_ref = db.collection('user').filter('name','==', name)
# #     doc = doc_ref.stream()

# #     if doc.exists:
# #         return doc.to_dict()
# #     else:
# #         raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")
    
# # 검색
# @router.get("/search")
# def search_resources():

#     return {"message": "Search"}

# # 학습목록 조회 
# @router.get("/study/{user_id}")
# def study_progress(user_id: str):
#     try:
#         # Firestore에서 유저의 UID로 연결된 학습 목록 가져오기
#         study_ref = db.collection('study').filter('user_id', '==', user_id)
#         study_docs = study_ref.stream()
        
#         # 학습 목록을 저장할 리스트 생성
#         study_list = []
        
#         for doc in study_docs:
#             study_data = doc.to_dict()
#             study_data['id'] = doc.id  # 문서 ID를 추가
#             study_list.append(study_data)
        
#         return {"studies": study_list}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"학습 목록을 가져오는 중 오류가 발생했습니다: {str(e)}")
    
# # 학습목록에서 삭제
# @router.delete("/study/delete ")
# def delete_study(study_ids: list[str], token: str = Depends(oauth2_scheme)):
#     user = get_current_user(token)
#     user_id = user.uid  # 토큰에서 추출한 UID
    
#     try:
#         # 특정 사용자에 대한 학습 중 주어진 SID 목록에 해당하는 학습 문서들을 가져오기
#         study_ref = db.collection('study')
#         query = study_ref.filter('user_id', '==', user_id).filter('study_id', 'in', study_ids)
#         study_docs = query.stream()

#         deleted_study_names = [] # 삭제된 학습의 이름을 저장할 리스트

#         for doc in study_docs:
#             study_data = doc.to_dict()
#             deleted_study_names.append(study_data.get('name'))  # 학습 이름 저장
#             doc.reference.delete()  # 문서 삭제

#         if not deleted_study_names:
#             raise HTTPException(status_code=404, detail="No studies found matching the provided IDs")

#         return {"message": f"Deleted {deleted_count} studies successfully"}

#     except HTTPException as http_err:
#         raise http_err
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred while deleting studies: {str(e)}")