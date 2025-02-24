from typing import Optional
from pydantic import BaseModel, Field


class CategoryBaseSchema(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    
    def dict(self):
        return self.model_dump()


class CategorySchema(CategoryBaseSchema):
    parent: Optional[str] = None
    sub_categories: Optional[list[str]] = Field(default_factory=list)


class CategorySchemaIn(CategorySchema):
    ...


class CategorySchemaOut(CategorySchemaIn):
    id: str


class CategorySchemaOutShort(CategoryBaseSchema):
    id: str
    slug: str = Field(exclude=True)


class CategoryUpdateSchema(CategorySchema):
    name: Optional[str] = None
    slug: Optional[str] = None
    sub_categories: Optional[list[str]] = None
    
    def dict(self):
        return self.model_dump(exclude_unset=True)