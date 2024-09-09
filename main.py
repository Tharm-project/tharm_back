from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth as firebase_auth
from firebase_set import db
from routes import user_routes, video_routes, study_routes

# FastAPI 인스턴스 생성
app = FastAPI()

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
async def home_page(user: firebase_auth.UserRecord = Depends(get_current_user)):
    # 메인 페이지(첫 화면): 현재 학습 중인 목록, 학습 목록 출력
    try:
        # 사용자 정보
        user_id = user.uid
        user_name = user.display_name or user.email

        # Firestore 내림차순 쿼리 작성 및 실행 (Query 없이)
        study_ref = db.collection('study').where('user_id', '==', user_id).order_by('created_at', direction='DESCENDING').limit(1)
        study_docs = study_ref.stream()

        # 학습 데이터 가져오기
        study_data = None
        for study_doc in study_docs:
            study_data = study_doc.to_dict()
            study_data['id'] = study_doc.id
            break

        if not study_data:
            raise HTTPException(status_code=404, detail="학습 데이터를 찾을 수 없습니다.")

        # 광고 정보 가져오기
        ads_ref = db.collection('AD')
        ads_docs = ads_ref.stream()

        ads_list = []
        for doc in ads_docs:
            ad_data = doc.to_dict()
            ad_data['id'] = doc.id
            ads_list.append(ad_data)

        return {
            "user": f"Welcome {user_name}!",
            "last_study": f"Last study is {study_data.get('name')}, and progress is {study_data.get('status')}",
            "advertisement": ads_list
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"홈페이지 로드 중 오류: {str(e)}")

# routes 쪼개기 및 dependencies를 통해 토큰 확인 함수 적용
app.include_router(user_routes, prefix="/user", tags=["User"], dependencies=[Depends(get_current_user)])
app.include_router(video_routes, prefix="/videos", tags=["Videos"], dependencies=[Depends(get_current_user)])
app.include_router(study_routes, prefix="/studies", tags=["Studies"], dependencies=[Depends(get_current_user)])