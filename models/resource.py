from typing import Dict, Optional
from uuid import UUID4
from ..schemas.schemas import ResourceSchema

class ResourceModel:
    def __init__(self):
        self.db: Dict[UUID4, ResourceSchema] = {}

    def add_resource(self, resource: ResourceSchema):
        self.db[resource.id] = resource

    def get_resource(self, resource_id: UUID4) -> Optional[ResourceSchema]:
        return self.db.get(resource_id)
