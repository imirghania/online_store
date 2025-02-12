from typing import Annotated, Optional
from beanie import Document, Indexed, Link, BackLink
from pydantic import Field
from schemas.category import CategorySchema

__all__ = ("CategoryModel",)

class CategoryModel(CategorySchema, Document):
    name: Annotated[str, Indexed(unique=True)]
    slug: Annotated[str, Indexed(unique=True)]
    parent: Optional[Link["CategoryModel"]] = None
    sub_categories: Optional[list[BackLink["CategoryModel"]]] = Field(
        original_field="parent",
        default_factory=list
        )

    class Settings:
        name = "categories"
        use_state_management = True

