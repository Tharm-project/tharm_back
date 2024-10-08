from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_set import db
from routes import user_routes, resource_routes, video_routes, study_routes
from controller import seeder
from firebase_set import initialize_firebase

# FastAPI 인스턴스 생성
app = FastAPI()

# Firebase 초기화 (필요한 경우)
if not firebase_admin._apps:
    initialize_firebase()

# firebase authentication으로 토큰을 확인하고 없으면 user/login으로 넘어가게 만든다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

# 토큰이 있는지 확인하는 함수
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        user = firebase_auth.get_user(decoded_token['uid'])
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {str(e)}")
    
# 홈 페이지
@app.get("/")
# async def home_page(user: firebase_auth.UserRecord = Depends(get_current_user)):
async def home_page():
    # 메인 페이지(첫 화면): 현재 학습 중인 목록, 학습 목록 출력
    try:
        # # 사용자 정보
        # user_id = user.uid
        # user_name = user.display_name or user.email

        # # Firestore 내림차순 쿼리 작성 및 실행 (Query 없이)
        # study_ref = db.collection('study').where('user_id', '==', user_id).order_by('created_at', direction='DESCENDING').limit(1)
        # study_docs = study_ref.stream()

        # # 학습 데이터 가져오기
        # study_data = None
        # for study_doc in study_docs:
        #     study_data = study_doc.to_dict()
        #     study_data['id'] = study_doc.id
        #     break

        # if not study_data:
        #     raise HTTPException(status_code=404, detail="학습 데이터를 찾을 수 없습니다.")

        # # 광고 정보 가져오기
        # ads_ref = db.collection('ad')

        # ads_docs = ads_ref.stream()

        # ads_list = []
        # for doc in ads_docs:
        #     ad_data = doc.to_dict()
        #     ad_data['id'] = doc.id
        #     ads_list.append(ad_data)

        # return {
        #     "user": f"Welcome {user_name}!",
        #     "last_study": f"Last study is {study_data.get('name')}, and progress is {study_data.get('status')}",
        #     "advertisement": ads_list
        # }
        return { "message": "welcome!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"홈페이지 로드 중 오류: {str(e)}")
    
# 시더파일 생성
async def lifespan(app):
    # 애플리케이션이 시작될 때 실행
    await seeder.seed_data()
    yield {"message":"시더 처리 완료, 애플리케이션 종료~~"}

# routes 쪼개기 및 dependencies를 통해 토큰 확인 함수 적용
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(resource_routes.router, prefix="/resource", tags=["Resource"])
app.include_router(video_routes.router, prefix="/videos", tags=["Videos"])
app.include_router(study_routes.router, prefix="/studies", tags=["Studies"])
# app.include_router(video_routes.router, prefix="/videos", tags=["Videos"], dependencies=[Depends(get_current_user)])
# app.include_router(study_routes.router, prefix="/studies", tags=["Studies"], dependencies=[Depends(get_current_user)])
