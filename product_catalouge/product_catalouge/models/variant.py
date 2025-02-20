from typing import Annotated
from beanie import Document, Indexed
from schemas.variant import VariantSchema



__all__ = ("VariantModel",)


class VariantModel(VariantSchema, Document):
    name: Annotated[str, Indexed(unique=True)]
    sku: Annotated[str, Indexed(unique=True)]

    class Settings:
        name = "variants"
        use_state_management = True