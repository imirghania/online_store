from dataclasses import dataclass, field
from numbers import Number
from typing import Optional


@dataclass
class Attribute:
    """docstring for Attribute."""
    id: str
    label: str
    type: str
    is_required: bool
    value: str | Number | list


@dataclass
class ProductType:
    """docstring for ProductType."""
    id: str
    name: str
    taxes_class: str
    general_attributes: Optional[list[Attribute]] = field(default_factory=list)
    variant_attributes: Optional[list[Attribute]] = field(default_factory=list)


class Category:
    """docstring for Category."""
    id: str
    name: str
    description: str
    parent = Optional["Category"] = None
    sub_categories: Optional[list["Category"]] = field(default_factory=list)


class Product:
    def __init__(self, name, description, product_type, category, media):
        ...


class Variant:
    def __init__(self, Name, sku, options, price, stock, media):
        ...