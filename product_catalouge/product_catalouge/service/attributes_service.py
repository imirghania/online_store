from product_catalouge.repository.base_repository import Repository
from .domain import Attribute


class AttributeService:
    def __init__(self, repository: Repository):
        self.repository = repository
    
    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, payload):
        return self.repository.create(payload, Attribute)