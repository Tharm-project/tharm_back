import os
from dotenv import load_dotenv

# .env 파일의 환경 변수를 로드
load_dotenv()

class Settings:
    FIREBASE_JSON: str = os.getenv('FIREBASE_JSON')
    FIREBASE_PROJECT_ID: str = os.getenv('FIREBASE_PROJECT_ID')

# 설정 객체 생성
settings = Settings()
