from fastapi import FastAPI
import firebase_set
from .routes.routes import router

# FastAPI 인스턴스 생성
app = FastAPI()

# 라우트 등록
app.include_router(router)

# Firebase 초기화 (필요한 경우)
firebase_set.initialize_firebase()