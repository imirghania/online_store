from numbers import Number
from typing import Annotated, Optional

from beanie import Document, Indexed, Link
from pydantic import Field

from product_catalouge.schemas.main import Image, Media, Price, Stock


__all__ = (
        "AttributeModel", 
        "ProductTypeModel", 
        "CategoryModel", 
        "MediaObjectModel",
        "ProductModel",
        "VariantModel",
        )


class AttributeModel(Document):
    label: str
    internal_code: Annotated[str, Indexed(unique=True)]
    type: str
    is_required: bool
    is_numeric: bool
    measurement_type: str
    unit: str
    value: str|Number|list

    class Settings:
        name = "attributes"
        use_state_management = True
    
    def dict(self):
        return {
            "id": self.id,
            "label": self.label, 
            "internal_code": self.internal_code, 
            "type": self.type, 
            "is_required": self.is_required, 
            "is_numeric": self.is_numeric, 
            "measurement_type": self.measurement_type, 
            "unit": self.unit, 
            "value": self.value, 
        }


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


class MediaObjectModel(Document):
    title: str
    slug: Annotated[str, Indexed(unique=True)]
    image: Image
    thumbnail: Image

    class Settings:
        name = "media_objects"
        use_state_management = True

    def dict(self):
        return {
            "id": self.id,
            "title": self.title, 
            "image": self.image.dump_model(), 
            "thumbnail": self.thumbnail.dump_model(), 
        }


class ProductModel(Document):
    name: str
    slug: Annotated[str, Indexed(unique=True)]
    product_type: Link[ProductTypeModel]
    categories: Optional[list[Link[CategoryModel]]] = Field(default_factory=list)
    channels: Optional[list[str]] = Field(default_factory=list)
    media = Optional[Media] = None

    class Settings:
        name = "products"
        use_state_management = True

    def dict(self):
        categories = [category.dict() for category in categories]
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug, 
            "product_type": self.product_type.dict(), 
            "categories": self.categories, 
            "channels": self.channels, 
            "media": self.media.dump_model(), 
        }


class VariantModel(Document):
    name: str
    slug: Annotated[str, Indexed(unique=True)]
    sku: str
    product: Link[ProductModel]
    attributes_selection: dict
    media = Optional[Media] = None
    stock: Optional[list[Stock]] = Field(default_factory=list)
    price: list[Price]

    class Settings:
        name = "variants"
        use_state_management = True

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug, 
            "sku": self.sku, 
            "product": self.product.dict(), 
            "attributes_selection": self.attributes_selection, 
            "media": self.media.dump_model(), 
            "stock": self.stock.dump_model(),
            "price": self.price.dump_model(),
        }