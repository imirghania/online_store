from typing import Any, Callable, Optional
from exceptions.database_exceptions import (DuplicateRecordError,
                                            InvalidInputError, RecordNotFound)
from exceptions.http_exceptions import (InvalidInputError_400,
                                        ItemAlreadyExistsError_409,
                                        ItemNotFoundError_404)
from schemas import BaseSchema
from product_catalouge.repository.base_repository import Repository
from product_catalouge.types import Model
from .domain import Domain


class Service:
    
    model_label = "Item" 
    
    def __init__(self, repository: Repository, domain_class: Domain):
        self.repository = repository()
        self.DomainClass = domain_class


    async def create(self, 
                    payload:BaseSchema, 
                    proccessor:Optional[Callable]=None
                    ) -> tuple[Domain, Any]:
        try:
            record = await self.repository.create(payload.dict())
            if proccessor:
                record = proccessor(record)
            return self.DomainClass(**record.dict()), record
        except DuplicateRecordError as e:
            print(f"[X][ERROR]: The {self.model_label} already exists")
            raise ItemAlreadyExistsError_409(self.model_label)


    async def get_one(self, 
                    id:str, 
                    proccessor:Optional[Callable]=None) -> Domain:
        record = await self.get_record(id)
        if proccessor:
            record = proccessor(record)
        return self.DomainClass(**record.dict())


    async def get_all(self, proccessor:Optional[Callable]=None) -> list[Domain]:
        items = await self.repository.get_all()
        print(f"[BASE SERVICE][GET-ALL]: {items}")
        if proccessor:
            items = [
                self.DomainClass(**proccessor(attr).dict()) for attr in items
                ] if items else []
        else:
            items = [
                self.DomainClass(**attr.dict()) for attr in items
                ] if items else []
        return items


    async def update_one(self, 
                        id:str, 
                        payload:BaseSchema, 
                        proccessor:Optional[Callable]=None) -> tuple[Domain, Any]:
        try:
            updated_record = await self.repository.update_one(id, payload.dict())
            print("="*100)
            print(f"[UPATED RECORD][{self.model_label}]: {updated_record}")
            if updated_record is None:
                raise ItemNotFoundError_404(self.model_label)
            if proccessor:
                record = proccessor(record)
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


    async def get_record(self, id:str) -> Model:
        try:
            record = await self.repository.get_one(id)
            if record is None:
                raise ItemNotFoundError_404(self.model_label)
            return record
        except InvalidInputError as e:
            raise InvalidInputError_400(self.model_label)