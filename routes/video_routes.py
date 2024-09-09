from fastapi import APIRouter, HTTPException, FastAPI
from firebase_set import db
from schemas.schemas import VideoSchema
from controller import video_controller, seeder

router = APIRouter()

#영상 저장
@router.post("/video")
def create_video(video: VideoSchema):
    # 일단 샘플 1개만 저장해보고 상세 구현 예정
    # 비동기 성능 처리 + 특정 시간마다, 특정 동작 반복 처리(트리거 또는 큐?가 여기도 있나?)
    doc_ref = db.collection("video").document(str(video.id))
    doc_ref.set(video)

    return {"message": "동영상 저장 완료!"}

#영상 출력
@router.get("/video/{video_id}")
def get_video(video_id: str):
    ref = db.collection("video").document(video_id)
    doc = ref.get()
    if doc.exists():
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Video not found.")

@router.post("/videos/update")
async def update_videos():
    return await video_controller.update_videos()

async def lifespan(app: FastAPI):
    # 애플리케이션이 시작될 때 실행
    await seeder.seed_data()
    yield {"message":"시더 처리 완료, 애플리케이션 종료~~"}
