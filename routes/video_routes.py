from fastapi import APIRouter, HTTPException
from firebase_set import db, bucket
from schemas.schemas import VideoSchema
from controller import video_controller
from datetime import datetime, timezone, timedelta
import requests

router = APIRouter()

#영상 저장
@router.post("/upload")
def create_video(video: VideoSchema):
    # 비동기 성능 처리 + 특정 시간마다, 특정 동작 반복 처리(트리거 또는 큐?가 여기도 있나?)
    try:
        # Firestore에 비디오 데이터 저장
        doc_ref = db.collection('video').document(str(video.id))
        doc_ref.set(video.model_dump())
        return {"message": "동영상 저장 완료!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"##Error saving video: {str(e)}")
    
#영상 요청
# 프론트에서 받은 텍스트를 ai서버에 동영상으로 만들어 달라고 요청 할 api
# ai서버로 부터 저장된 동영상에 대한 메타데이터를 받아올 예정
@router.post("/testupload")
def request_video(text: str):
    try:
        # return video_controller.new_videos_save(text)
        
        # 더미데이터를 버킷 어디에 저장할지 지정
        dummy_video = bucket.blob(f"video/3.mp4")

        # 동영상이 이미 존재하는지 확인
        if dummy_video.exists():
            return {"message": "뭐야! 이미 있자나"}
        # 없으면 새로 추가하기
        with open('/Users/kimjiseong/Portproject/Thame/tharm_back/video/2.mp4', 'rb') as video_file:
            dummy_video.upload_from_file(video_file)
        
        # 동영상 URL 생성
        video_url = dummy_video.generate_signed_url(timedelta(seconds=3600))

        # Firestore 컬렉션에서 새 문서 생성
        video_ref = db.collection('video').document()

        # Firestore에 저장할 더미데이터 생성
        video_data = {
            "id": video_ref.id,
            "url": video_url,  # 생성된 동영상 URL
            "title": text,  # 프론트에서 받은 텍스트를 제목으로 저장
            "total_time": 1,  # 총 재생 시간 (0으로 기본 설정)
            "watch_status": False,  # 시청 상태 초기값
            "created_at": datetime.now(timezone.utc), # "id": dummy_video.id if dummy_video.id else "Q34sdjke"  id가 None일 수 있으므로 빈 문자열로 처리
            "last_watch_time": datetime.now(timezone.utc), 
            "updated_at": datetime.now(timezone.utc),  # 업데이트 시간도 기본값 설정
        }
        # Firestore에 동영상 데이터 저장
        video_ref.set(video_data)

        return {'message':'더미 성공', 'response': video_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving video: {str(e)}")
        
#영상 출력
@router.get("/{video_id}")
def get_video(video_id: str):
    try:
        # storage 버킷에서 동영상 파일 가져오기
        video_doc_ref = db.collection('video').document(video_id)
        video_doc = video_doc_ref.get()

        # 문서가 존재하는지 확인
        if not video_doc.exists:
            raise HTTPException(status_code=404, detail="동영상을 찾을 수 없습니다.")

        video_data = video_doc.to_dict()
        video_url = video_data['url']
        
        # URL 유효성 확인
        try:
            response = requests.head(video_url)
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="유효하지 않은 동영상 URL입니다.")
        except requests.RequestException:
            new_video_url = video_controller.regenerate_video_url(video_data['title'])
            video_data['url'] = new_video_url
            video_doc_ref.update({
                'url': new_video_url, 
                'updated_at': datetime.now(timezone.utc),
                'watch_status': True,
                })
            return {
                'message': "동영상 url초기화 및 가져오기 성공",
                "video_data": video_data
            }
        
        # 동영상 시청시간 변경
        if video_data['watch_status']:
            video_doc_ref.update({
                "last_watch_time": datetime.now(timezone.utc), 
            })
        else: 
            video_doc_ref.update({
                'updated_at': datetime.now(timezone.utc),
                "last_watch_time": datetime.now(timezone.utc), 
                'watch_status': True,
            })
        
        # 유효한 경우 동영상 정보 반환
        return {
            "message": "동영상 정보 가져오기 성공",
            "video_data": video_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"비디오를 찾을 수 없습니다.: {str(e)}")

#영상 수정
@router.post("/update")
async def update_videos(title: str, video: VideoSchema):
    try:
        videos_ref = db.collection('video')
        query = videos_ref.where('title', '==', title).limit(1)
        docs = query.stream()
        doc = next(docs, None)
        
        if not doc:
            raise HTTPException(status_code=404, detail="비디오를 찾을 수 없습니다.")

        # 비디오 데이터 업데이트
        doc.reference.update(video.model_dump(exclude_unset=True))
        return {"message": "영상 데이터 업데이트 성공!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"##Error updating video: {str(e)}")
