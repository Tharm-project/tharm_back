import os
import yaml
import firebase_admin
from firebase_admin import storage, credentials, firestore, auth

def initialize_firebase():
    try:
        # 환경 변수에서 자격 증명 파일 경로 가져옴
        with open('config.yml','r') as file:
            config = yaml.safe_load(file)

        # Firebase 설정 정보 추출
        cred_path = config['firebase']['json_path']
        storage_bucket =  config['firebase']['storage_bucket']

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

        # Firebase가 이미 초기화되어 있는지 확인
        if not firebase_admin._apps:
            if cred_path:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'storageBucket': storage_bucket
                })
                print("Firebase 초기화 완료!")
            else:
                raise ValueError("FIREBASE_JSON 환경 변수가 설정되지 않았습니다.")
        else:
            print("Firebase는 이미 초기화되었습니다.")
    except Exception as e:
        raise ValueError(f"Firebase 초기화 중 오류 발생: {e}")

# Firebase 초기화 함수 호출
initialize_firebase()

# Firestore와 Storage 클라이언트 초기화
db = firestore.client()
bucket = storage.bucket()  # storage.bucket()은 기본적으로 초기화된 버킷을 사용

__all__ = ["auth", "firestore", "storage"]
