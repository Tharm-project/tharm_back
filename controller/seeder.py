from datetime import datetime, timezone
from pydantic import UUID4
from firebase_admin import firestore

db = firestore.client()

async def seed_data():
    # todo: 최초에 ai -> 모델로 서빙된다고 했는데, 받을 값 형식 성윤님과 체크 필요
    # 일단 시더부분은 firestore에서 업로드 된 딕셔너리 내 컬렉션 값을 받아와 씀.
    videos_ref = db.collection("videos")
    docs = videos_ref.stream()
    title_data = docs.title
    url_data = docs.url
    total_time = docs.total_time 
    print(title_data, url_data, total_time)
    if not docs:
        init_video = [
            {
                "id": UUID4(),
                # "study_id": UUID4(),
                # "resource_id": UUID4(),
                "title": title_data,
                "url": url_data,
                "total_time": total_time,
                "watch_status": False,
                "created_at": datetime.now(timezone.utc)
            },
        ]
        for video in init_video:
            videos_ref.document(str(video["id"])).set(video)
        return {"message": "시더가 성공적으로 실행되었습니다"}
    return {"message": "시더가 필요하지 않습니다. 데이터가 이미 존재합니다."}
