from base_repository import Repository
from models import ProductModel
from models import Product


class ProdutRepository(Repository):
    async def __init__(self):
        super().__init__(ProductModel)
    
    async def create(self, payload):
        record = await self.model(**payload)
        return ProductModel(record.dict())