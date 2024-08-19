from fastapi import APIRouter, FastAPI, HTTPException, Depends
from firebase_set import auth, firestore
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from schemas.schemas import UserSchema, Token, VideoSchema, ResourceSchema
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from controller import video_controller, seeder

app = FastAPI()
router = APIRouter()

# Firebase Firestore 클라이언트 연결
db = firestore.client()

#datetime format set
def format_datetime(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# 비밀번호 Hash 처리
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 비밀번호 검증
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # 토큰 검증
        decoded_token = auth.verify_id_token(token)
        user = auth.get_user(decoded_token['uid'])
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@router.get("/")
def home_page():
    # 메인 페이지(첫화면)은 현재 학습 중인 목록, 학습 목록 출력
    return {"message": "welcome to Tharm"}

# 회원가입
@router.post("/create/user")
async def create_new_user(create_user: UserSchema):
    try:
        hashed_password = hash_password(create_user.password) #해쉬처리한 비밀번호로 저장
        # 이후 비밀번호 찾기 시엔 이메일 체크 후 비밀번호 재설정으로 넘기기
        # 비밀번호 원본 데이터는 우리도 모르기 때문
        
        # Firestore에 사용자 저장 (id는 Firebase Auth에서 생성된 uid로 설정)
        user_data = {
            "email": create_user.email,
            "name": create_user.name,
            "phone": create_user.phone,
            "password": hashed_password,
            "created_at": format_datetime(create_user.created_at) if create_user.created_at else None,
        }

        # Firebase Authentication에 사용자 생성 (비밀번호는 저장되지 않음)
        user_record = auth.create_user(
            email=create_user.email,
            display_name=create_user.name,
            disabled=False
        )
        
        # Firestore에 사용자의 uid를 키로 하여 데이터 저장
        db.collection('users').document(user_record.uid).set(user_data)

        return {"message": "회원가입 생성 완료!", "user_data": jsonable_encoder(user_data)} #추후 프론트에서 필요한 값 있는지 체크(문구 등)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 로그인
@router.post("/user/login", response_model=Token)
def login(data: UserSchema):
    try:
        # Firebase Admin SDK로 사용자 찾기
        user = auth.get_user_by_email(data.email)
        
        if not user:
            raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 유효하지 않습니다.")

        # Firestore에서 사용자 데이터 가져오기
        user_ref = db.collection('users').document(user.uid)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise HTTPException(status_code=400, detail="사용자가 존재하지 않습니다.")

        user_data = user_doc.to_dict()
        hashed_password = user_data.get('password')  # 키 이름을 'password'로 사용

        # 비밀번호 검증
        if not pwd_context.verify(data.password, hashed_password):
            raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 유효하지 않습니다.")

        # 비밀번호가 일치하면 커스텀 토큰 생성
        custom_token = auth.create_custom_token(user.uid)
        
        # Token 스키마로 반환
        return Token(access_token=custom_token.decode('utf-8'), token_type="Bearer")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#아이디, 비밀번호 찾기
@router.get("/find/id")
def find_user(user_id:str):
    try:
        doc_ref = db.collection("users").document(user_id)
        user_doc = doc_ref.get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

        user_data = user_doc.to_dict()
        # print(user_data)
        return user_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 비밀번호 재설정 요청
@router.post("/find/reset-password")
async def reset_password(data: UserSchema):
    try:
        # Firebase Authentication을 사용하여 비밀번호 재설정 링크를 이메일로 전송
        # Todo: 재설정 메일 테스트 필요
        
        auth.send_password_reset_email(data.email)
        return {"message": "비밀번호 재설정 메일을 발송하였습니다."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}")
def get_user(user_id: str):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
# 검색
@router.get("/search")
def search_resources():

    return {"message": "Search"}

# 학습목록 조회 
@router.get("/list")
def study_progress():

    return {"message": "Study"}

# 파일 업로드
# todo: 최우선 순위임
@router.get("/resource")
def get_resource():
    #pdf, 사진 파일 업로드 기능 구현 -> 문장 추출 -> 오차율 확인 및 저장 구현하기
    return {"message": "Resource"}

@router.post("/videos")
async def create_video(video: VideoSchema):
    await video_controller.create_video(video.model_dump())
    return {"message": "Video saved successfully!"}

@router.get("/videos/{video_id}")
async def get_video(video_id: str):
    ref = db.collection("videos").document(video_id)
    doc = ref.get()
    if doc.exists():
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Video not found.")

@router.post("/videos/update")
async def update_videos():
    return await video_controller.update_videos()

async def lifespan(app: FastAPI):
    # 애플리케이션이 시작될 때 실행
    await seeder.seed_data()
    yield {"message":"시더 처리 완료, 애플리케이션 종료~~"}
    