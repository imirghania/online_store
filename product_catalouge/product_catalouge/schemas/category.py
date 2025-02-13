from typing import Optional
from pydantic import BaseModel, Field


class CategoryBaseSchema(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    
    def dict(self):
        return self.model_dump()


class CategorySchemaIn(CategoryBaseSchema):
    parent: Optional[str] = None
    sub_categories: Optional[list[str]] = Field(default_factory=list)


class CategorySchema(CategorySchemaIn):
    ...


class CategorySchemaOut(CategorySchema):
    id: str


class CategoryUpdateSchema(CategorySchema):
    name: Optional[str] = None
    slug: Optional[str] = None
    sub_categories: Optional[list[str]] = None
    
    def dict(self):
        return self.model_dump(exclude_unset=True)