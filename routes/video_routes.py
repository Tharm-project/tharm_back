from fastapi import APIRouter, HTTPException
from firebase_set import db
from schemas.schemas import VideoSchema
from controller import video_controller

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

#영상 출력
@router.get("/{video_id}")
def get_video(video_id: str):
    ref = db.collection('video').document(video_id)
    doc = ref.get()
    if doc.exists():
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="비디오를 찾을 수 없습니다.")

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
