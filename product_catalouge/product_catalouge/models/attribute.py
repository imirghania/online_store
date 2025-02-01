from typing import Annotated, Optional
from . import AttributeType, MeasurmentType
from beanie import Document, Indexed


__all__ = ("AttributeModel",)


class AttributeModel(Document):
    label: str
    internal_code: Annotated[str, Indexed(unique=True)]
    type: AttributeType = AttributeType.STRING
    is_required: bool
    is_numeric: bool = False
    measurement_type: Optional[MeasurmentType] = None
    unit: Optional[str] = None
    options: Optional[list] = None

    class Settings:
        name = "attributes"
        use_state_management = True
    
    def dict(self):
        return self.model_dump()