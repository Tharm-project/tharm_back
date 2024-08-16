import os
from firebase_admin import credentials, initialize_app


# Firebase 인증서 경로 설정
FIREBASE_JSON = os.path.join(os.path.dirname(__file__), '/Users/jeewoo-kim/projects/Tharm/tharm_back/firebase_set/firebase_credentials.json')

def initialize_firebase():
    cred_path = os.getenv('FIREBASE_JSON')
    if not cred_path:
        raise ValueError("FIREBASE_JSON environment variable not set")
    cred = credentials.Certificate(cred_path)
    initialize_app(cred)
