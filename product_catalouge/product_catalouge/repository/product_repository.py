from .base_repository import Repository
from models.product import ProductModel


class ProductRepository(Repository):
    model = ProductModel
    def __init__(self):
        super().__init__(self.model)