from copy import copy
from .base_repository import Repository
from models.attribute import AttributeModel


class AttributeRepository(Repository):
    model = AttributeModel
    def __init__(self):
        super().__init__(self.model)

    async def create(self, payload):
        processed_payload = self.process_payload(payload)
        record = self.model(**processed_payload)
        print(f"[RECORD]: {record}")
        return record
    
    @staticmethod
    def process_payload(payload):
        data = copy(payload)
        
        if data["is_numeric"] is False:
            keys_to_none = {"measurement_type", "unit"}
            for key in keys_to_none:
                data[key] = None 
        
        data["options"] = ( None 
                        if data["type"].value != "select"       # data["type"] is an Enum
                        else data["options"]
                        )
        
        return data