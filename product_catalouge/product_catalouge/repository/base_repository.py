from typing import Type

from beanie import Document, PydanticObjectId
from exceptions.database_exceptions import (
    DuplicateRecordError, RecordNotFound, InvalidInputError)
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError


class Repository:
    def __init__(self, model: Type[Document]):
        self.model = model
    
    async def create(self, payload: dict):
        try:
            record = self.model(**payload)
            await record.insert()
        except DuplicateKeyError as e:
            raise DuplicateRecordError
        print(f"[RECORD]: {record}")
        return record
    
    async def get_by_id(self, id: PydanticObjectId):
        try:
            return await self.model.get(id)
        except ValidationError as e:
            raise InvalidInputError

    async def get_all(self, filters: dict = None):
        filters = filters or {}
        return await self.model.find(filters).to_list()

    async def delete(self, id: PydanticObjectId):
        try:
            document = await self.get_by_id(id)
            await document.delete()
        except AttributeError as e:
            raise RecordNotFound