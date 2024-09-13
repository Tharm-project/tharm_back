import firebase_admin
from firebase_admin import storage, initialize_app, credentials
import os

def initialize_firebase():
    try:
        # 환경 변수에서 자격 증명 파일 경로 가져옴
        cred_path = os.getenv("FIREBASE_JSON")
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

        # Firebase가 이미 초기화 되어 있는지 확인
        if not firebase_admin._apps:
            if cred_path:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print("Firebase 초기화!")
            else:
                raise ValueError("FIREBASE_JSON 환경 변수가 설정되지 않았습니다.")
    except Exception as e:
        raise ValueError(f"Error initializing Firebase: {e}")

initialize_firebase()

# Firebase Storage에 파일 업로드
# bucket = storage.bucket('custom-bucket')
# blob = bucket.blob('path/to/file')
# blob.upload_from_filename('local/path/to/file')