from typing import Type
from beanie import Document, PydanticObjectId


class Repository:
    def __init__(self, model: Type[Document]):
        self.model = model
    
    async def get(self, id: PydanticObjectId):
        return await self.model.get(id)

    async def get_all(self, filters: dict = None):
        filters = filters or {}
        return await self.model.find(filters).to_list()

    async def delete(self, document: Document):
        await document.delete()