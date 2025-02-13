from typing import Annotated
from beanie import Document, Indexed
from schemas.category import CategorySchema

__all__ = ("CategoryModel",)

class CategoryModel(CategorySchema, Document):
    name: Annotated[str, Indexed(unique=True)]
    slug: Annotated[str, Indexed(unique=True)]

    class Settings:
        name = "categories"
        use_state_management = True

