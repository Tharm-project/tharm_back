from uuid import UUID4
from datetime import datetime
from datetime import datetime, timezone
from typing import List, Dict
from ..schemas.schemas import StudySchema
from ..schemas.schemas import ResourceSchema

class StudyController:
    def __init__(self):
        self.study_db: Dict[UUID4, StudySchema] = {}
        self.resource_db: Dict[UUID4, ResourceSchema] = {}

    def add_resource(self, resource: ResourceSchema):
        self.resource_db[resource.id] = resource
        if resource.study_id not in self.study_db:
            # 새로운 study_id로 Study 생성
            # created_at 날짜를 "YYYY-MM-DD" 형식으로 변환 후 제목으로 사용
            date_str = resource.created_at.strftime('%Y-%m-%d')
            
            # Study 이름 생성
            study_name = f"{date_str} _ {resource.url}"
            
            # StudySchema 인스턴스 생성 및 저장
            self.study_db[resource.study_id] = StudySchema(
                id=resource.study_id,
                user_id=resource.user_id,
                name=study_name,  # 생성된 이름 사용
                summary="",
                status=0.0,
                created_at=resource.created_at
            )

    def get_study_list(self, user_id: UUID4) -> List[StudySchema]:
        # user_id가 일치하는 모든 Study를 반환
        return [study for study in self.study_db.values() if study.user_id == user_id]

