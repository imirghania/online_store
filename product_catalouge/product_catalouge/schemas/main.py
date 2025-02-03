from decimal import Decimal
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
    quantity: Optional[int] = 0


class Price(BaseModel):
    channel_id: str
    currency: str
    amount: Decimal
    amount_discounted: Optional[Decimal] = None
