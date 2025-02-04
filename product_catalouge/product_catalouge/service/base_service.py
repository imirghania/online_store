from exceptions.database_exceptions import (
    DuplicateRecordError, RecordNotFound, InvalidInputError)
from exceptions.http_exceptions import (
    ItemNotFoundError_404, ItemAlreadyExistsError_409, InvalidInputError_400)
from fastapi import Response, status
from models.attribute import AttributeModel
from product_catalouge.repository.base_repository import Repository
from .domain import Attribute, Domain



class Service:
    
    __model_label__ = "Item" 
    
    def __init__(self, repository: Repository, domain_class: Domain):
        self.repository = repository()
        self.DomainClass = domain_class
    
    async def get_all(self):
        items = await self.repository.get_all()
        items = [
            self.DomainClass(**attr.dict()) for attr in items
            ] if items else []
        return items

    async def get_by_id(self, id):
        try:
            record = await self.repository.get_by_id(id)
            if record is None:
                raise ItemNotFoundError_404(self.__model_label__)
            return self.DomainClass(**record.dict())
        except InvalidInputError as e:
            raise InvalidInputError_400(self.__model_label__)

    async def create(self, payload: AttributeModel):
        try:
            record = await self.repository.create(payload.dict())
        except DuplicateRecordError as e:
            print(f"[X][ERROR]: The {self.__model_label__} already exists")
            raise ItemAlreadyExistsError_409(self.__model_label__)
        return Attribute(**record.dict())

    async def delete_by_id(self, id):
        try:
            await self.repository.delete(id)
        except RecordNotFound as e:
            raise ItemNotFoundError_404(self.__model_label__)
        return Response(status_code=status.HTTP_204_NO_CONTENT)