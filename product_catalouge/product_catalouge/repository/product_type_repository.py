from base_repository import Repository
from models import ProductTypeModel
from service.domain import ProductType


class ProductTypeRepository(Repository):
    def __init__(self):
        super.__init__(ProductTypeModel)
    
    async def create(self, payload: dict):
        record = await self.model(**payload)
        return ProductType(**record.dict())