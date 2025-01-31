from product_catalouge.repository.base_repository import Repository
from models.attribute import AttributeModel
from .domain import Attribute
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException, status


class AttributeService:
    def __init__(self, repository: Repository):
        self.repository = repository()
    
    async def get_all(self):
        attributes = await self.repository.get_all()
        attributes = [
            Attribute(**attr.model_dump()) for attr in attributes
            ] if attributes else []
        return attributes

    async def get_by_id(self, id):
        record = await self.repository.get_by_id(id)
        return Attribute(**record.model_dump())

    async def create(self, payload: AttributeModel):
        record = await self.repository.create(payload.model_dump())
        try:
            await record.insert()
        except DuplicateKeyError as e:
            print("[X][ERROR]: The Attribute name is already TAKEN")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="The attribute name is already taken")
        return Attribute(**record.model_dump())