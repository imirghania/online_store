from typing import Annotated, Optional

from beanie import Document, Indexed


__all__ = ("AttributeModel",)


class AttributeModel(Document):
    label: str
    internal_code: Annotated[str, Indexed(unique=True)]
    type: str
    is_required: bool
    is_numeric: bool
    measurement_type: str
    unit: Optional[str] = None
    value: str|int|float|list

    class Settings:
        name = "attributes"
        use_state_management = True
    
    def dict(self):
        return {
            "id": self.id,
            "label": self.label, 
            "internal_code": self.internal_code, 
            "type": self.type, 
            "is_required": self.is_required, 
            "is_numeric": self.is_numeric, 
            "measurement_type": self.measurement_type, 
            "unit": self.unit, 
            "value": self.value, 
        }