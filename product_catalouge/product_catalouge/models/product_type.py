from models.attribute import Annotated, Document, Indexed
from schemas.product import ProductTypeSchema

__all__ = ("ProductTypeModel",)


class ProductTypeModel(ProductTypeSchema, Document):
    name: Annotated[str, Indexed(unique=True)]

    class Settings:
        name = "product_types"
        use_state_management = True