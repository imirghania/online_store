from typing import Annotated
from beanie import Document, Indexed
from schemas.product import ProductSchema



__all__ = ("ProductModel",)


class ProductModel(ProductSchema, Document):
    name: Annotated[str, Indexed(unique=True)]

    class Settings:
        name = "products"
        use_state_management = True


