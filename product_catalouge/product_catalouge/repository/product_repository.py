from base_repository import Repository
from models import Product


class ProdutRepository(Repository):
    def __init__(self):
        super().__init__(Product)
    
    def create_attribute(self, arg):
        pass