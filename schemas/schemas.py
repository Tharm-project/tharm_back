from pydantic import BaseModel, EmailStr, UUID4, Json
from typing import List, Optional
from datetime import date, datetime

# User 스키마
class UserSchema(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    password: str
    phone: str
    created_at: date

# Study 스키마
class StudySchema(BaseModel):
    id: UUID4
    user_id: UUID4
    name: str
    summary: str
    status: float # 소수점 자리...를 넣는다면이니까 일단 float!
    created_at: date

# Resource 스키마
class ResourceSchema(BaseModel):
    id: UUID4
    study_id: UUID4
    url: str
    sentence: Json # { 'data' : ["문장", ... ]} 이런식으로 들어오니 Json!
    total: int
    last_idx: int
    created_at: date

# Search 스키마
class SearchSchema(BaseModel):
    id: UUID4
    query: str
    date: date

# Video 스키마
class VideoSchema(BaseModel):
    id: UUID4
    study_id: UUID4
    url: str
    title: str
    total_time: int
    last_watch_time: Optional[datetime] = None   # 기본을 None으로, 시간을 넣어야해서 datatime으로 넣음
    watch_status: bool
    created_at: date
    updated_at: date

# AD 스키마
class ADSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    url: str
    advertiser: Optional[str] = None # 광고주가 없을 수 있으니까 기본을 None으로!
