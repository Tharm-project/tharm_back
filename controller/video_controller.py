from datetime import datetime, timezone
from pydantic import UUID4
from fastapi import HTTPException
from firebase_admin import firestore, storage
from kiwipiepy import Kiwi
import httpx

db = firestore.client()
bucket = storage.bucket()  # Firebase Storage 버킷 객체

#영상의 메타데이터를 Firestore에 저장
def save_video_metadata_to_firebase(video_data):
    try:
        video_data['created_at'] = datetime.now(timezone.utc)
        db.collection('video').document(str(video_data['id'])).set(video_data)
        return {"message": "비디오 메타데이터 Firestore에 저장"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def new_videos_save(text: str):
    try:
        # AI 모델로부터 데이터 수신
        ai_server = "히히"
        payload = {"text": text} 
        
        # http 요청
        # AI 서버에 데이터 요청
        async with httpx.AsyncClient(verify=False) as client:   # httpx SSL 인증서 우회
            response = await client.post(ai_server, json=payload)

        # 응답 확인
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="AI 서버 응답 오류")

        ai_data = response.json()

        new_video = {
            # "id": UUID4(), -> 데이터 저장시 추가로 넣어줘야함
            # "study_id": UUID4(),
            # "resource_id": UUID4(),
            "url": ai_data.url,
            "title": ai_data.title,
            "total_time": ai_data.total_time,
            "width": ai_data.width,
            "height": ai_data.height,
            "fps": ai_data.fps,
            "watch_status": False,
            "created_at": datetime.now(timezone.utc)
        }

        print('## new video 데이터 확인: ', new_video)

        # Firestore에 메타데이터 저장 -> ai 서버에서 firestroe로 바로 저장해준다고 합니다!!
        # save_video_metadata_to_firebase(new_video)

        return {"message": "비디오 메타데이터 및 문장 데이터 처리 완료"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# url 새로 만드는 함수
def regenerate_video_url(doc_id: str):
    video = bucket.blob(f"video/{doc_id}.mp4")
    new_video_url = video.generate_signed_url(expiration=3600)
    return new_video_url