from typing import Dict, Optional
from uuid import uuid4
from schemas.schemas import ResourceSchema

class ResourceModel:
    def __init__(self):
        self.db: Dict[uuid4, ResourceSchema] = {}

    def add_resource(self, resource: ResourceSchema):
        self.db[resource.id] = resource

    def get_resource(self, resource_id: uuid4) -> Optional[ResourceSchema]:
        return self.db.get(resource_id)
