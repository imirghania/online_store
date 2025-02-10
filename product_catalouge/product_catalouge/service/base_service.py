from typing import Any
from exceptions.database_exceptions import (DuplicateRecordError,
                                            InvalidInputError, RecordNotFound)
from exceptions.http_exceptions import (InvalidInputError_400,
                                        ItemAlreadyExistsError_409,
                                        ItemNotFoundError_404)
from schemas import BaseSchema
from product_catalouge.repository.base_repository import Repository
from .domain import Domain


class Service:
    
    model_label = "Item" 
    
    def __init__(self, repository: Repository, domain_class: Domain):
        self.repository = repository()
        self.DomainClass = domain_class

    async def get_all(self) -> list[Domain]:
        items = await self.repository.get_all()
        items = [
            self.DomainClass(**attr.dict()) for attr in items
            ] if items else []
        return items

    async def get_one(self, id:str) -> Domain:
        try:
            record = await self.repository.get_one(id)
            if record is None:
                raise ItemNotFoundError_404(self.model_label)
            return self.DomainClass(**record.dict())
        except InvalidInputError as e:
            raise InvalidInputError_400(self.model_label)

    async def create(self, payload:BaseSchema) -> tuple[Domain, Any]:
        try:
            record = await self.repository.create(payload.dict())
            return self.DomainClass(**record.dict()), record
        except DuplicateRecordError as e:
            print(f"[X][ERROR]: The {self.model_label} already exists")
            raise ItemAlreadyExistsError_409(self.model_label)

    async def update_one(self, id:str, payload:BaseSchema) -> tuple[Domain, Any]:
        try:
            updated_record = await self.repository.update_one(id, payload.dict())
            print(f"[UPATED RECORD]: {updated_record}")
            if updated_record is None:
                raise ItemNotFoundError_404(self.model_label)
            return self.DomainClass(**updated_record.dict()), updated_record
        except RecordNotFound as e:
            raise ItemNotFoundError_404(self.model_label)
        except InvalidInputError as e:
            raise InvalidInputError_400(self.model_label)
        except DuplicateRecordError as e:
            raise ItemAlreadyExistsError_409(self.model_label)

    async def delete_one(self, id:str):
        try:
            await self.repository.delete_one(id)
        except RecordNotFound as e:
            raise ItemNotFoundError_404(self.model_label)