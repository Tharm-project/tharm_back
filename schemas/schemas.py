from pydantic import BaseModel, EmailStr, Json
from typing import List, Optional
from datetime import datetime

# User 스키마
class UserSchema(BaseModel):
    # id: UUID4
    name: str
    email: EmailStr
    password: str
    phone: str 
    created_at: Optional[datetime] = None 

# 로그인 스키마
class loginSchema(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    
# Study 스키마 (학습)
class StudySchema(BaseModel):
    id: str
    user_id: str
    name: str
    summary: str
    status: float # 소수점 자리...를 넣는다면이니까 일단 float!
    created_at: Optional[datetime] = None 

# Resource 스키마(pdf, image 파일)
class ResourceSchema(BaseModel):
    id: str
    user_id: str
    study_id: str
    url: str #pdf/file에 대한 url
    sentence: Json # { 'data' : ["문장", ... ]} 이런식으로 들어오니 Json!
    total: int #전체 단어수
    last_idx: int #마지막 단어/문장 위치
    created_at: Optional[datetime] = None

# Search 스키마
class SearchSchema(BaseModel):
    id: str
    user_id: str
    resource_id:str
    query: str #검색 문장
    date: datetime #조회 일자

# Video 스키마 (영상)
class VideoSchema(BaseModel):
    id: str
    study_id: str
    resource_id: str
    title: str #영상 제목
    url: str
    total_time: int #총 재생시간
    last_watch_time: Optional[datetime] = None   # 기본을 None으로, 시간을 넣어야해서 datatime으로 넣음
    watch_status: bool #시청 유무
    created_at: datetime
    updated_at: Optional[datetime] = None

# AD 스키마
class ADSchema(BaseModel):
    id: str
    user_id: str
    url: str
    advertiser: Optional[str] = None # 광고주가 없을 수 있으니까 기본을 None으로!
    click_num: int #클릭 수(추후 광고 받으면 사용)
    impressions: int #노출 수(추후 광고 받으면 사용)
    return_num: int #반환 수(추후 광고 받으면 사용)

# 아이디 검색 스키마
class UserSearchSchema(BaseModel):
    name: str
    phone: str

# 패스워드 찾기 스키마
class PasswordResetSchema(BaseModel):
    email: str