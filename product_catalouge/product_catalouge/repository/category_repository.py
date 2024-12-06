from base_repository import Repository
from models import CategoryModel
from service.domain import Category


class ProductTypeRepository(Repository):
    def __init__(self):
        super.__init__(CategoryModel)
    
    async def create(self, payload: dict):
        record = await self.model(**payload)
        return Category(record.dict())