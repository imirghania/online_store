from typing import Annotated
from schemas.attribute import AttributeSchema
from beanie import Document, Indexed


__all__ = ("AttributeModel",)


class AttributeModel(AttributeSchema, Document):
    internal_code: Annotated[str, Indexed(unique=True)]

    class Settings:
        name = "attributes"
        use_state_management = True
