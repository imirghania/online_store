from exceptions.database_exceptions import (
    DuplicateRecordError, RecordNotFound, InvalidInputError)
from exceptions.http_exceptions import (
    create_ItemNotFoundError_404, create_ItemAlreadyExistsError_409, InvalidInput_400)
from fastapi import HTTPException, Response, status
from models.attribute import AttributeModel
from product_catalouge.repository.base_repository import Repository
from .domain import Attribute


AttributeNotFound_404 = create_ItemNotFoundError_404("Attribute")
AttributeAlreadyExists_409 = create_ItemAlreadyExistsError_409("Attribute")


class AttributeService:
    def __init__(self, repository: Repository):
        self.repository = repository()
    
    async def get_all(self):
        attributes = await self.repository.get_all()
        attributes = [
            Attribute(**attr.dict()) for attr in attributes
            ] if attributes else []
        return attributes

    async def get_by_id(self, id):
        try:
            record = await self.repository.get_by_id(id)
            if record is None:
                raise AttributeNotFound_404
            return Attribute(**record.dict())
        except InvalidInputError as e:
            raise InvalidInput_400

    async def create(self, payload: AttributeModel):
        try:
            record = await self.repository.create(payload.dict())
        except DuplicateRecordError as e:
            print("[X][ERROR]: The Attribute name is already TAKEN")
            raise AttributeAlreadyExists_409
        return Attribute(**record.dict())

    async def delete_by_id(self, id):
        try:
            await self.repository.delete(id)
        except RecordNotFound as e:
            raise AttributeNotFound_404
        return Response(status_code=status.HTTP_204_NO_CONTENT)