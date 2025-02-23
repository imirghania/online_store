from typing import Literal
from beanie import PydanticObjectId
from exceptions.database_exceptions import InvalidInputError
from product_catalouge.repository.product_repository import ProductRepository
from product_catalouge.service.categories_service import categories_service
from product_catalouge.service.media_service import media_service
from product_catalouge.service.product_type_service import product_type_service
from .base_service import Service
from .domain import Product


class ProductService(Service):
    model_label = "Product"
    def __init__(self, repository: ProductRepository):
        super().__init__(repository, Product)
        self.product_type_service = product_type_service
        self.media_service = media_service
        self.categories_service = categories_service
    
    
    async def get_one_verbose(self, id: PydanticObjectId):
        product = await self.get_one(id)
        product.product_type = (await self.product_type_service.get_one_verbose(
            product.product_type
        )).dict()
        product.main_media = (await self.media_service.get_one(
            product.main_media
        )).dict()
        product.media_gallery = [
            (await self.media_service.get_one(media_id)).dict() 
            for media_id in product.media_gallery
            ]
        product.categories = [
            (await self.categories_service.get_one(cat_id)).dict() 
            for cat_id in product.categories
            ]
        return product
    
    
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




product_service = ProductService(ProductRepository)