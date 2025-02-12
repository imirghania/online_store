from typing import Optional
from pydantic import BaseModel


class CategoryBaseSchema(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    
    def dict(self):
        return self.model_dump()


class CategorySchemaIn(CategoryBaseSchema):
    parent: Optional[str] = None
    sub_categories: Optional[list[str]] = None


class CategorySchema(CategoryBaseSchema):
    parent: Optional["CategorySchema"] = None
    sub_categories: Optional[list[str]] = None


class ParentCategory(BaseModel):
    id: str
    name: str


class CategorySchemaOut(CategorySchema):
    id: str
    parent: Optional[ParentCategory] = None


class CategoryUpdateSchema(CategorySchemaIn):
    name: Optional[str] = None
    slug: Optional[str] = None
    
    def dict(self):
        return self.model_dump(exclude_unset=True)