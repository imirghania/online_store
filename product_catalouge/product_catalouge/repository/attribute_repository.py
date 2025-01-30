from .base_repository import Repository
from models.attribute import AttributeModel
from service.domain import Attribute


class AttributeRepository(Repository):
    def __init__(self):
        super.__init__(AttributeModel)
    
    async def create(self, payload: dict):
        record = await self.model(**payload)
        return Attribute(**record.dict())