from dataclasses import asdict, dataclass, field
from typing import Optional, Protocol


@dataclass
class Domain(Protocol):
    def dict(self):
        ...


@dataclass
class Attribute:
    """docstring for Attribute."""
    id: str
    label: str
    internal_code: str
    type: str
    is_required: bool
    is_numeric: bool | None
    measurement_type: str | None
    unit: str | None
    options: list | None
    
    def dict(self):
        data = asdict(self)
        data["id"] = str(self.id)
        if self.is_numeric is False:
            keys_to_remove = {"measurement_type", "unit"}
            data = {
                key: value for key, value in data.items() 
                    if key not in keys_to_remove
                }
        
        if self.type != "select":
            data.pop("options", None)
        
        return data


@dataclass
class Category:
    """docstring for Category."""
    id: str
    name: str
    slug: str
    description: str
    parent: Optional[str] = None
    sub_categories: Optional[list[str]] = field(default_factory=list)
    
    def dict(self):
        data = asdict(self)
        data["id"] = str(self.id)
        return data


@dataclass
class ProductType:
    """docstring for ProductType."""
    id: str
    name: str
    taxes_class: str
    general_attributes: Optional[list[str]] = field(default_factory=list)
    variant_attributes: Optional[list[str]] = field(default_factory=list)
    
    def dict(self):
        data = asdict(self)
        data["id"] = str(self.id)
        return data


@dataclass
class Image:
    """docstring for Image."""
    url: str
    alt: str
    width: int
    height: int

    # def dict(self):
    #     return asdict(self)


@dataclass
class Media:
    """docstring for Media."""
    id: str
    title: str
    image: Image
    thumbnail: Optional[Image] = None
    
    def dict(self):
        data = asdict(self)
        data["id"] = str(self.id)
        # data["image"]["url"] = str(data["image"]["url"])
        return data


# @dataclass
# class Product:
#     """docstring for Product."""
#     id: str
#     name: str
#     slug: str
#     product_type: str
#     categories: Optional[list[Category]] = field(default_factory=list)
#     channels: Optional[list[str]] = field(default_factory=list)
#     media: Optional[Media] = None

#     def dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "slug": self.slug,
#             "product_type": self.product_type.dict(),
#             "categories": [category.dict() for category in self.categories],
#             "media": self.media.model_dump(),
#         }


# @dataclass
# class Variant:
#     """docstring for Variant."""
#     name: str
#     slug: str
#     sku: str
#     product: Product
#     attributes_selection: dict
#     price: list[Price]
#     media: Optional[Media] = None
#     stock: Optional[list[Stock]] = field(default_factory=list)

#     def dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "slug": self.slug,
#             "sku": self.sku,
#             "product": self.product.dict(),
#             "attributes_selection": self.attributes_selection,
#             "media": self.media.model_dump(),
#             "stock": self.stock.model_dump(),
#             "price": self.price.model_dump(),
#         }