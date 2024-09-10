from fastapi import APIRouter, HTTPException
from firebase_set import db
from schemas.schemas import VideoSchema
from controller import video_controller

router = APIRouter()

#영상 저장
@router.post("/upload")
def create_video(video: VideoSchema):
    # 일단 샘플 1개만 저장해보고 상세 구현 예정
    # 비동기 성능 처리 + 특정 시간마다, 특정 동작 반복 처리(트리거 또는 큐?가 여기도 있나?)
    doc_ref = db.collection("video").document(str(video.id))
    doc_ref.set(video)

    return {"message": "동영상 저장 완료!"}

#영상 출력
@router.get("/{video_id}")
def get_video(video_id: str):
    ref = db.collection("video").document(video_id)
    doc = ref.get()
    if doc.exists():
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Video not found.")

@router.post("/update")
async def update_videos(text: str):
    return await video_controller.update_videos(text)
