import firebase_admin
from firebase_admin import storage, initialize_app

def initialize_firebase():
    try:
        if not firebase_admin._apps:
            initialize_app()
    except Exception as e:
        raise ValueError(f"Error initializing Firebase: {e}")

initialize_firebase()

# Firebase Storage에 파일 업로드
bucket = storage.bucket()
blob = bucket.blob('path/to/file')
blob.upload_from_filename('local/path/to/file')