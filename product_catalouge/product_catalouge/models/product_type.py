from typing import Optional

from beanie import Link
from models.attribute import AttributeModel, Annotated, Document, Indexed
from pydantic import Field

__all__ = ("ProductTypeModel",)

class ProductTypeModel(Document):
    name: Annotated[str, Indexed(unique=True)]
    taxes_class: str
    general_attributes: Optional[list[Link[AttributeModel]]] = Field(default_factory=list)
    variant_attributes: Optional[list[Link[AttributeModel]]] = Field(default_factory=list)

    class Settings:
        name = "product_types"
        use_state_management = True

    def dict(self):
        return {
            "id": self.id,
            "name": self.name, 
            "taxes_class": self.taxes_class, 
            "general_attributes": [atr.dict() for atr in self.general_attributes], 
            "variant_attributes": [atr.dict() for atr in self.variant_attributes],
        }