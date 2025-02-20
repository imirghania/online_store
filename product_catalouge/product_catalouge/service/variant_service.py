from product_catalouge.repository.variant_repository import(
    VariantRepository)
from exceptions.database_exceptions import InvalidInputError
from beanie import PydanticObjectId
from typing import Literal
from .base_service import Service
from .domain import Variant



class VariantService(Service):
    model_label = "Variant"
    def __init__(self, repository: VariantRepository):
        super().__init__(repository, Variant)
    
    
    async def add_item(self, 
                    id: PydanticObjectId, 
                    item_id: PydanticObjectId,
                    item_type: Literal['category', 'channel', 'media']):
        product_record = await super().get_record(id)
        if item_type.lower() == 'category':
            product_record.categories.append(item_id)
        elif item_type.lower() == 'channel':
            product_record.channels.append(item_id)
        elif item_type.lower() == 'media':
            product_record.media_gallery.append(item_id)
        
        updated_product = self.DomainClass(**product_record.dict())
        
        return updated_product, product_record


    async def remove_item(self, 
                    id: PydanticObjectId, 
                    item_id: PydanticObjectId,
                    item_type: Literal['category', 'channel', 'media']):
        product_record = await super().get_record(id)
        if item_type.lower() == 'category':
            try:
                product_record.categories.remove(item_id)
            except ValueError as e:
                raise InvalidInputError("Category")
        elif item_type.lower() == 'channel':
            try:
                product_record.channels.remove(item_id)
            except ValueError as e:
                raise InvalidInputError("Channel")
        elif item_type.lower() == 'media':
            try:
                product_record.media_gallery.remove(item_id)
            except ValueError as e:
                raise InvalidInputError("Media")
        
        updated_product = self.DomainClass(**product_record.dict())
        
        return updated_product, product_record


