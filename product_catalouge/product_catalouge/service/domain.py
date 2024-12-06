from dataclasses import dataclass, field
from numbers import Number
from typing import Optional

from product_catalouge.schemas import Image, Media, Price, Stock


@dataclass
class Attribute:
    """docstring for Attribute."""
    id: str
    label: str
    type: str
    is_required: bool
    value: str | Number | list
    
    def dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "type": self.type,
            "is_required": self.is_required,
            "value": self.value,
        }


@dataclass
class ProductType:
    """docstring for ProductType."""
    id: str
    name: str
    taxes_class: str
    general_attributes: Optional[list[Attribute]] = field(default_factory=list)
    variant_attributes: Optional[list[Attribute]] = field(default_factory=list)
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "taxes_class": self.taxes_class,
            "general_attributes": [atr.dict() for atr in self.general_attributes],
            "variant_attributes": [atr.dict() for atr in self.variant_attributes],
        }


@dataclass
class Category:
    """docstring for Category."""
    id: str
    name: str
    description: str
    parent = Optional["Category"] = None
    sub_categories: Optional[list["Category"]] = field(default_factory=list)
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parent": self.parent.dict(),
            "sub_categories": [category.dict() for category in self.sub_categories],
        }


@dataclass
class MediaObject:
    """docstring for Category."""
    id: str
    title: str
    image: Image
    thumbnail: Image

    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "thumbnail": self.thumbnail,
        }


@dataclass
class Product:
    """docstring for Product."""
    id: str
    name: str
    slug: str
    product_type: str
    categories: Optional[list[Category]] = field(default_factory=list)
    channels: Optional[list[str]] = field(default_factory=list)
    media = Optional[Media] = None

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "product_type": self.product_type.dict(),
            "categories": [category.dict() for category in self.categories],
            "media": self.media.model_dump(),
        }


@dataclass
class Variant:
    """docstring for Variant."""
    name: str
    slug: str
    sku: str
    product: Product
    attributes_selection: dict
    media = Optional[Media] = None
    stock: Optional[list[Stock]] = field(default_factory=list)
    price: list[Price]

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "sku": self.sku,
            "product": self.product.dict(),
            "attributes_selection": self.attributes_selection,
            "media": self.media.model_dump(),
            "stock": self.stock.model_dump(),
            "price": self.price.model_dump(),
        }