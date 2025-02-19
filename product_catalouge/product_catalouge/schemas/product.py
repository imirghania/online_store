from typing import Optional
from pydantic import BaseModel, Field



class ProductSchema(BaseModel):
    name: str
    product_type: str
    categories: Optional[list[str]] = Field(default_factory=list)
    channels: Optional[list[str]] = Field(default_factory=list)
    main_media: Optional[str] = None
    media_gallery: Optional[list[str]] = Field(default_factory=list)
    
    def model_post_init(self, __context) -> None:
        self.categories = list(set(self.categories))
        self.channels = list(set(self.channels))
        self.media_gallery = list(set(self.media_gallery))
    
    def dict(self):
        return self.model_dump()


class ProductSchemaIn(ProductSchema):
    ...


class ProductSchemaOut(ProductSchema):
    id: str


class ProductSchemaUpdate(ProductSchema):
    name: Optional[str] = None
    product_type: Optional[str] = None
    
    def dict(self):
        return self.model_dump(exclude_unset=True)