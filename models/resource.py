from typing import Dict, Optional
from schemas.schemas import ResourceSchema

class ResourceModel:
    def __init__(self):
        self.db: Dict[str, ResourceSchema] = {}

    def add_resource(self, resource: ResourceSchema):
        self.db[resource.id] = resource

    def get_resource(self, resource_id: str) -> Optional[ResourceSchema]:
        return self.db.get(resource_id)
