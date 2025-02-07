from typing import Optional, Literal
from pydantic import BaseModel, Field


AttributeType = Literal['select', 'number', 'string']
MeasurementType = Literal['distance', 'weight', 'volume']


class AttributeSchema(BaseModel):
    label: str
    internal_code: str
    type: AttributeType = "string"
    is_required: bool
    is_numeric: bool = Field(default=False, init=False)
    measurement_type: Optional[MeasurementType] = None
    unit: Optional[str] = None
    options: Optional[list] = None
    
    def model_post_init(self, __context) -> None:
        self.is_numeric = True if self.type.lower() == "number" else False
    
    def dict(self):
        return self.model_dump()


class AttributeUpdateSchema(AttributeSchema):
    label: Optional[str] = None
    internal_code: Optional[str] = None
    type: Optional[AttributeType] = None 
    is_required: Optional[bool] = None
    # is_numeric: Optional[bool] = None
    
    def dict(self):
        return self.model_dump(exclude_unset=True)