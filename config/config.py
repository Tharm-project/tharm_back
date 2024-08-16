from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

class Settings:
    FIREBASE_JSON: str = os.getenv("FIREBASE_JSON")

settings = Settings()