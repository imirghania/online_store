from decimal import Decimal
from numbers import Number
from typing import Optional
from pydantic import BaseModel, Field


class Image(BaseModel):
    url: str
    width: int
    width: int
    alt: Optional[str] = None


class MediaObject(BaseModel):
    title: str
    image: Image
    thumbnail: Image


class Media(BaseModel):
    items: Optional[list[MediaObject]] = Field(default_factory=list)
    main_media: Optional[MediaObject] = None
    thumbnail: Optional[MediaObject] = None


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