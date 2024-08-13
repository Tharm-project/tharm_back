import firebase_admin
from firebase_admin import credentials
from config.config import settings

def initialize_firebase():
    # 환경 변수에서 인증서 경로를 가져옴
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_JSON)
        firebase_admin.initialize_app(cred)

initialize_firebase()