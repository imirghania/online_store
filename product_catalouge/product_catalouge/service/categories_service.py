from typing import Any
from beanie import PydanticObjectId
from schemas.category import CategorySchemaIn
from product_catalouge.repository.base_repository import Repository
from .base_service import Service
from .domain import Category


class CategoryService(Service):
    model_label = "Category"
    def __init__(self, repository: Repository):
        super().__init__(repository, Category)

    async def create(self, payload: CategorySchemaIn) -> tuple[Category, Any]:
        category, record = await super().create(payload)
        parent = (
            await self.repository.get_one(str(category.parent))
            if category.parent is not None
            else None
            )
        print(f"[PARENT]: {parent}")
        if parent is not None:
            parent.sub_categories.append(str(category.id))
        return category, record, parent

    async def delete_one(self, id:PydanticObjectId):
        objects_to_track = []
        category = await self.repository.get_one(id)
        if (parent_id:= category.parent) is not None:
            print(f"[PARENT-ID]: {parent_id}")
            parent_record = await self.repository.get_one(str(parent_id))
            print(f"[CATEGORY PARENT]: {parent_record}")
            print(f"[PARENT][SUB-CATEGORIES]: {parent_record.sub_categories}")
            print(f"[CATEGORY ID]: {id}")
            parent_record.sub_categories.remove(id)
            objects_to_track.append(parent_record)
        if category.sub_categories:
            for id_ in category.sub_categories:
                sub = await self.repository.get_one(id_)
                sub.parent = (
                    str(parent_id) 
                    if parent_id is not None 
                    else None
                    )
                objects_to_track.append(sub)
        await category.delete()
        return objects_to_track