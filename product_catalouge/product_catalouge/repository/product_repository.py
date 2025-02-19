from base_repository import Repository
from models import ProductModel


class ProdutRepository(Repository):
    model = ProductModel
    async def __init__(self):
        super().__init__(self.model)