from product_catalouge.repository.base_repository import Repository


class AttributeService:
    def __init__(self, repository: Repository):
        self.repository = repository
    
    def get_by_id(self, id):
        self.repository.get_by_id(id)

    def create(self, payload):
        self.repository.create(payload)