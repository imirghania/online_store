from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Optional, Protocol


@dataclass
class Domain(Protocol):
    def dict(self):
        ...


@dataclass
class BaseDomain:
    id: str
    
    def dict(self):
        data = asdict(self)
        data["id"] = str(self.id)
        return data


@dataclass
class Attribute(BaseDomain):
    """docstring for Attribute."""
    label: str
    internal_code: str
    type: str
    is_required: bool
    is_numeric: bool | None
    measurement_type: str | None
    unit: str | None
    options: list | None
    
    def dict(self):
        data = super().dict()
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
class Category(BaseDomain):
    """docstring for Category."""
    name: str
    slug: str
    description: str
    parent: Optional[str] = None
    sub_categories: Optional[list[str]] = field(default_factory=list)


@dataclass
class ProductType(BaseDomain):
    """docstring for ProductType."""
    name: str
    taxes_class: str
    general_attributes: Optional[list[str]] = field(default_factory=list)
    variant_attributes: Optional[list[str]] = field(default_factory=list)


@dataclass
class Image:
    """docstring for Image."""
    url: str
    alt: Optional[str]
    width: int
    height: int


@dataclass
class Media(BaseDomain):
    """docstring for Media."""
    title: str
    image: Image
    thumbnail: Optional[Image] = None


@dataclass
class Product(BaseDomain):
    """docstring for Product."""
    name: str
    product_type: str
    categories: Optional[list[str]] = field(default_factory=list)
    channels: Optional[list[str]] = field(default_factory=list)
    main_media: Optional[str] = None
    media_gallery: Optional[list[str]] = None


@dataclass
class Stock:
    iventory_id: str
    quantity: Optional[int] = 0


@dataclass
class Price:
    channel_id: str
    currency: str
    amount: Decimal
    amount_discounted: Optional[Decimal] = 0.00


@dataclass
class Variant(BaseDomain):
    """docstring for Variant."""
    name: str
    sku: str
    product: Product
    attributes_selection: dict
    main_media: Optional[str]
    media_gallery: Optional[list[str]]
    price: list[Price]
    stock: Optional[list[Stock]] = field(default_factory=list)