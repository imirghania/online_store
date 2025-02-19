from .base_repository import Repository
from models.product_type import ProductTypeModel


class ProductTypeRepository(Repository):
    model = ProductTypeModel
    def __init__(self):
        super().__init__(self.model)