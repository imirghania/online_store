# from typing import Annotated, Optional

# from beanie import Document, Indexed, Link
# from models.product import ProductModel
# from pydantic import Field

# from product_catalouge.schemas.main import Media, Price, Stock


# __all__ = ("VariantModel",)


# class VariantModel(Document):
#     name: str
#     slug: Annotated[str, Indexed(unique=True)]
#     sku: str
#     product: Link[ProductModel]
#     attributes_selection: dict
#     media = Optional[Media] = None
#     stock: Optional[list[Stock]] = Field(default_factory=list)
#     price: list[Price]

#     class Settings:
#         name = "variants"
#         use_state_management = True

#     def dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "slug": self.slug, 
#             "sku": self.sku, 
#             "product": self.product.dict(), 
#             "attributes_selection": self.attributes_selection, 
#             "media": self.media.dump_model(), 
#             "stock": self.stock.dump_model(),
#             "price": self.price.dump_model(),
#         }