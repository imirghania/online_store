from typing import Type, Protocol
from beanie import Document, PydanticObjectId
from .exceptions import DocumentNotFound


class DomainClass(Protocol):
    id: str
    
    def dict(self):
        ...
    

class Repository:
    def __init__(self, model: Type[Document]):
        self.model = model
    
    async def create(self, payload: dict, domain_class: DomainClass):
        record = await self.model(**payload)
        return domain_class(**record.dict())
    
    async def get_by_id(self, id: PydanticObjectId):
        return await self.model.get(id)

    async def get_all(self, filters: dict = None):
        filters = filters or {}
        return await self.model.find(filters).to_list()

    async def delete(self, id: PydanticObjectId):
        document = self.get_by_id(id)
        if not document:
            raise DocumentNotFound
        await document.delete()