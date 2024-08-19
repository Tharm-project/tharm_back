from datetime import datetime, timezone
from pydantic import UUID4
from fastapi import HTTPException
from firebase_admin import firestore, storage
import requests
import os

db = firestore.client()
bucket = storage.bucket()  # Firebase Storage 버킷 객체

#비디오 파일을 다운로드하여 로컬 파일 시스템에 저장
def download_video(video_url, local_path):
    try:
        response = requests.get(video_url)
        with open(local_path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def upload_video_to_firebase(local_path, video_data):
    try:
        # Firebase Storage에 비디오 업로드
        blob = bucket.blob(f"videos/{video_data['id']}.mp4")
        blob.upload_from_filename(local_path)
        video_data['url'] = blob.public_url

        # Firestore에 비디오 데이터 저장
        video_data['created_at'] = datetime.now(timezone.utc)
        db.collection("videos").document(str(video_data['id'])).set(video_data)
        return {"message": "업로드한 비디오가 Firestore에 저장됨"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # finally:
    #     # 로컬 파일 삭제 
    #     # 사장된 단어,정확도가 낮은 경우...로컬까지 없앨 일은 잘 없을 것 같아서 일단 주석~
    #     if os.path.exists(local_path):
    #         os.remove(local_path)
    #         return {"message":"업로드 후, 로컬 파일 삭제~"}

#영상의 메타데이터를 Firestore에 저장
def save_video_directly_to_firebase(video_data):
    try:
        video_data['created_at'] = datetime.now(timezone.utc)
        db.collection("videos").document(str(video_data['id'])).set(video_data)
        return {"message": "비디오 관련 정보 Firestore에 저장(비디오 자체는 로컬에 존재)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_videos():
    try:
        # AI 모델로부터 데이터 수신
        #todo: ai_data는 성윤님께서 전달 주실 값 예제입니다
        #일단 정말 대강 만들었읍니다. 모양은 달라도 괜찮아요!
        ai_data = [
            {"title": "시(poem)", "url": "어쩌구저쩌구11.mp4", "total_time": 2100},
            {"title": "노래(song)", "url": "exampl22.mp4", "total_time": 1800},
            {"title": "영화(movie)", "url": "movie123.mp4", "total_time": 2400},
        ]
        
        for data in ai_data:
            title_ref = data['title']
            url_ref = data['url']
            total_time = data['total_time']

        new_video = {
            "id": UUID4(),
            # "study_id": UUID4(),
            # "resource_id": UUID4(),
            "title": title_ref,
            "url": url_ref,
            "total_time": total_time,
            "watch_status": False,
            "created_at": datetime.now(timezone.utc)
        }

        #로컬에 저장 후 Firebase에 업로드
        #todo: 성윤님, local_path 로컬에 영상 저장할 경로도 지정 부탁드려요~
        local_path = f"/tmp/{new_video['id']}.mp4" 
        download_video(new_video['url'], local_path)
        return upload_video_to_firebase(local_path, new_video)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
