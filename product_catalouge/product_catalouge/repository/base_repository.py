from typing import Type, Any

from beanie import Document, PydanticObjectId
from exceptions.database_exceptions import (
    DuplicateRecordError, RecordNotFound, InvalidInputError)
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError


class Repository:
    def __init__(self, model: Type[Document]):
        self.model = model
    
    async def create(self, payload:dict):
        try:
            record = self.model(**payload)
            await record.insert()
            return record
        except DuplicateKeyError as e:
            print(f"[DUPLICATE-KEY ERROR]: {e.details}")
            raise DuplicateRecordError

    async def get_one(self, id:PydanticObjectId):
        try:
            return await self.model.get(id)
        except ValidationError as e:
            print(f"[INVALID-INPUT ERROR]: {e}")
            raise InvalidInputError

    async def get_all(self, filters: dict = None):
        filters = filters or {}
        return await self.model.find(filters).to_list()

    async def update_one(self, id:PydanticObjectId, payload:dict[str, Any]):
        try:
            document = await self.get_one(id)
            print(f"[REPOSITORY][DOCUMENT][BASE]: {document}")
            if not document:
                raise RecordNotFound
            
            for key, value in payload.items():
                setattr(document, key, value)
            
            print(f"[REPOSITORY][DOCUMENT][UPDATED]: {document}")
            # await document.save()
            return document
        except ValidationError as e:
            raise InvalidInputError
        except DuplicateKeyError as e:
            raise DuplicateRecordError

    async def delete_one(self, id:PydanticObjectId):
        try:
            document = await self.get_one(id)
            await document.delete()
        except AttributeError as e:
            raise RecordNotFound