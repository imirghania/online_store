from decimal import Decimal
from typing import Annotated,Optional
from pydantic import BaseModel, Field, BeforeValidator


DecimalType = Annotated[Decimal, BeforeValidator(lambda x: Decimal(str(x)))]


class Stock(BaseModel):
    iventory_id: str
    quantity: Optional[int] = 0


class Price(BaseModel):
    channel_id: str
    currency: str
    amount: DecimalType
    amount_discounted: Optional[DecimalType] = 0.00


class VariantSchema(BaseModel):
    name: str
    sku: str
    product: str
    attributes_selection: dict
    main_media: Optional[str] = None
    media_gallery: Optional[list[str]] = Field(default_factory=list)
    stock: list[Stock]
    price: list[Price]
    
    def model_post_init(self, __context) -> None:
        self.media_gallery = (list(set(self.media_gallery)) 
                            if self.media_gallery is not None 
                            else []) 
    
    def dict(self):
        return self.model_dump()


class VariantSchemaIn(VariantSchema):
    ...


class VariantSchemaOut(VariantSchema):
    id: str


class VariantSchemaUpdate(VariantSchema):
    name: Optional[str] = None
    sku: Optional[str] = None
    product: Optional[str] = None
    attributes_selection: Optional[dict] = None
    media_gallery: Optional[list[str]] = None
    stock: Optional[list[Stock]] = None
    price: Optional[list[Price]] = None
    
    def dict(self):
        return self.model_dump(exclude_unset=True)