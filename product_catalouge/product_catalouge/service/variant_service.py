from typing import Literal
from beanie import PydanticObjectId
from exceptions.database_exceptions import InvalidInputError
from product_catalouge.repository.variant_repository import VariantRepository
from .base_service import Service
from .domain import Variant
from .media_service import media_service
from .product_service import product_service


class VariantService(Service):
    model_label = "Variant"
    def __init__(self, repository: VariantRepository):
        super().__init__(repository, Variant)
        self.product_service = product_service
        self.media_service = media_service
    
    
    async def get_one_verbose(self, id: PydanticObjectId):
        variant = await super().get_one(id)
        print(f"[VARIANT][VERBOSE]: {variant}")
        product, main_media, media_gallery = await self.get_details(variant)
        print("="*100)
        print(f"[VARIANT][VERBOSE][PRODUCT]: {product}")
        print("="*100)
        print(f"[VARIANT][VERBOSE][MAIN-MEDIA]: {main_media}")
        print("="*100)
        print(f"[VARIANT][VERBOSE][MEDIA-GALLERY]: {media_gallery}")
        
        variant.product = product
        variant.main_media = main_media
        variant.media_gallery = media_gallery
        
        return variant
    
    
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
    
    
    async def get_details(self, variant_object):
        main_media = (await media_service.get_one(variant_object.main_media)).dict()
        media_gallery = [
            (await media_service.get_one(meida_id)).dict() 
            for meida_id in variant_object.media_gallery
            ]
        product = (await product_service.get_one_verbose(variant_object.product)).dict()
        
        return product, main_media, media_gallery


