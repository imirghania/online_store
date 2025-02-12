from copy import copy
import asyncio
from typing import Any
from beanie import Link
from exceptions.database_exceptions import (DuplicateRecordError,
                                            InvalidInputError, RecordNotFound)
from exceptions.http_exceptions import (InvalidInputError_400,
                                        ItemAlreadyExistsError_409,
                                        ItemNotFoundError_404)
from schemas.category import CategorySchemaIn
from product_catalouge.repository.base_repository import Repository
from .base_service import Service
from .domain import Category


class CategoryService(Service):
    model_label = "Category"
    def __init__(self, repository: Repository):
        super().__init__(repository, Category)

    async def create(self, payload: CategorySchemaIn) -> tuple[Category, Any]:
        try:
            record = await self.repository.create(payload.dict())
            await record.fetch_all_links()
            formated_record = self.format(record)
            return self.DomainClass(**formated_record.dict()), record
        except DuplicateRecordError as e:
            print(f"[X][ERROR]: The {self.model_label} already exists")
            raise ItemAlreadyExistsError_409(self.model_label)

    async def get_one(self, id:str) -> Category:
        record = await super().get_one(id, needs_format=True)
        return record

    async def get_all(self) -> list[Category]:
        categories = await super().get_all(needs_format=True)
        categories = [
            await cat.parent.fetch()  
            if type(cat.parent) == Link 
            else cat
            for cat in categories
            ]
        print("="*100)
        print(f"[CATEGORY SERVICE][GET-ALL]: {categories}")
        print("="*100)
        return categories


    def format(self, record):
        output = copy(record)
        print("="*100)
        print(f"[CATEGORY SERVICE][FORMAT][BEFORE]: {record}")
        print("="*100)
        if output.parent:
            output.parent.id = str(output.parent.id)
            output.parent.sub_categories = [
                str(cat.id) for cat in output.parent.sub_categories
                ]
            output.parent = output.parent.dict()
        if output.sub_categories:
            output.sub_categories = [str(sub.id) for sub in output.sub_categories]
        print(f"[CATEGORY SERVICE][FORMAT][AFTER]: {record}")
        return output