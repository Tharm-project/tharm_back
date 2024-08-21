from firebase_set import db
from datetime import datetime
from uuid import UUID4

class VideoModel:
    def __init__(self, id: UUID4, study_id: UUID4, url:str, total_time: int, watch_status: str, last_watch_time:datetime, created_at: datetime, updated_at:datetime):
        self.id = id
        self.study_id = study_id
        self.url = url
        self.total_time: total_time
        self.last_watch_time = last_watch_time
        self.watch_status = watch_status
        self.created_at = created_at
        self.updated_at = updated_at