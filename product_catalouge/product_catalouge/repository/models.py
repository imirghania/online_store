from decimal import Decimal
from typing import Optional
from numbers import Number
from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field


class AttributeModel(Document):
    label: str
    internal_code: str
    type: str
    is_required: bool
    is_numeric: bool
    measurement_type: str
    unit: str
    value: str|list|Number

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
    name: str
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
    name: str
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


class Image(BaseModel):
    url: str
    width: int
    width: int
    alt: Optional[str] = None


class MediaObjectModel(Document):
    title: str
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


class MediaModel(Document):
    items: Optional[list[Link[MediaObjectModel]]] = Field(default_factory=list)
    main_media: Optional[Link[MediaObjectModel]] = None
    thumbnail: Optional[Link[MediaObjectModel]] = None

    class Settings:
        name = "media"
        use_state_management = True

    def dict(self):
        items = [item.dict() for item in items]
        main_media = main_media.dict() if main_media else None
        thumbnail = thumbnail.dict() if thumbnail else None
        return {
            "id": self.id,
            "items": self.items, 
            "main_media": self.main_media, 
            "thumbnail": self.thumbnail, 
        }


class ProductModel(Document):
    name: str
    slug: str
    product_type: Link[ProductTypeModel]
    categories: Optional[list[Link[CategoryModel]]] = Field(default_factory=list)
    channels: Optional[list[str]] = Field(default_factory=list)
    media = Optional[MediaModel] = None

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
            "media": self.media.dict(), 
        }

class Stock(BaseModel):
    iventory_id: str
    quantity: Optional[Number] = 0


class Price(BaseModel):
    channel_id: str
    currency: str
    amount: Decimal
    amount_discounted: Optional[Decimal] = None


class AttributeSelection(BaseModel):
    attribute_name: str
    value: str


class Variant(Document):
    name: str
    slug: str
    sku: str
    product: Link[ProductModel]
    attributes_selection: dict
    media = Optional[MediaModel] = None
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
            "media": self.media.dict(), 
            "stock": self.stock.dump_model(),
            "price": self.price.dump_model(),
        }