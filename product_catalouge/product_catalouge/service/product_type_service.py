from typing import Literal
from beanie import PydanticObjectId
from exceptions.database_exceptions import InvalidInputError
from product_catalouge.repository.product_type_repository import(
    ProductTypeRepository)
from .base_service import Service
from .domain import ProductType



class ProductTypeService(Service):
    model_label = "ProductType"
    def __init__(self, repository: ProductTypeRepository):
        super().__init__(repository, ProductType)
    
    
    async def add_attribute(self, 
                    id: PydanticObjectId, 
                    attribute_id: PydanticObjectId,
                    attribute_type: Literal['general', 'variant']):
        product_type_record = await super().get_record(id)
        if attribute_type.lower() == 'general':
            product_type_record.general_attributes.append(attribute_id)
        elif attribute_type.lower() == 'variant':
            product_type_record.variant_attributes.append(attribute_id)
        
        updated_product_type = self.DomainClass(**product_type_record.dict())
        
        return updated_product_type, product_type_record


    async def remove_attribute(self, 
                    id: PydanticObjectId, 
                    attribute_id: PydanticObjectId,
                    attribute_type: Literal['general', 'variant']):
        product_type_record = await super().get_record(id)
        if attribute_type.lower() == 'general':
            try:
                product_type_record.general_attributes.remove(attribute_id)
            except ValueError as e:
                raise InvalidInputError("Attribute")
        elif attribute_type.lower() == 'variant':
            try:
                product_type_record.variant_attributes.remove(attribute_id)
            except ValueError as e:
                raise InvalidInputError("Attribute")
        
        updated_product_type = self.DomainClass(**product_type_record.dict())
        
        return updated_product_type, product_type_record


