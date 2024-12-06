from typing import Annotated, Optional
from beanie import Document, Indexed, Link


__all__ = ("CategoryModel",)


class CategoryModel(Document):
    name: Annotated[str, Indexed(unique=True)]
    slug: Annotated[str, Indexed(unique=True)]
    description: str
    parent = Optional[Link["CategoryModel"]] = None
    sub_categories: Optional[list[Link["CategoryModel"]]] = None

    class Settings:
        name = "categories"
        use_state_management = True

    def dict(self):
        sub_categories = (
            [atr.dict() for atr in self.sub_categories] 
            if self.sub_categories else None
            )
        return {
            "id": self.id,
            "name": self.name, 
            "description": self.description, 
            "parent": self.parent.dict(), 
            "sub_categories": sub_categories,
        }