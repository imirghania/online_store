from typing import Optional, Literal
from pydantic import BaseModel


AttributeType = Literal['select', 'number', 'string']
MeasurementType = Literal['distance', 'weight', 'volume']


class AttributeSchema(BaseModel):
    label: str
    internal_code: str
    type: AttributeType = "string"
    is_required: bool
    is_numeric: bool = False
    measurement_type: Optional[MeasurementType] = None
    unit: Optional[str] = None
    options: Optional[list] = None
    
    def dict(self):
        return self.model_dump()