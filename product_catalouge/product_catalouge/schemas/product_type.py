from typing import Optional
from pydantic import BaseModel, Field
from .attribute import AttributeSchemaIn, AttributeSchemaNoInternalCode



class ProductTypeSchema(BaseModel):
    name: str
    taxes_class: str
    general_attributes: Optional[list[str]] = Field(default_factory=list)
    variant_attributes: Optional[list[str]] = Field(default_factory=list)
    
    def model_post_init(self, __context) -> None:
        self.general_attributes = list(set(self.general_attributes))
        self.variant_attributes = list(set(self.variant_attributes))
    
    def dict(self):
        return self.model_dump()


class ProductTypeSchemaIn(ProductTypeSchema):
    ...


class ProductTypeSchemaOut(ProductTypeSchema):
    id: str


class ProductTypeSchemaUpdate(ProductTypeSchema):
    name: Optional[str] = None
    taxes_class: Optional[str] = None
    
    def dict(self):
        return self.model_dump(exclude_unset=True)


class ProductTypeSchemaOutDetailed(ProductTypeSchemaOut):
    id: str = Field(exclude=True)
    general_attributes: Optional[list[AttributeSchemaIn]]
    variant_attributes: Optional[list[AttributeSchemaIn]]
    
    def model_post_init(self, __context) -> None:
        ...


class ProductTypeSchemaOutNoInternalCode(ProductTypeSchemaOutDetailed):
    general_attributes: Optional[list[AttributeSchemaNoInternalCode]]
    variant_attributes: Optional[list[AttributeSchemaNoInternalCode]]
    