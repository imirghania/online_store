from .base_repository import Repository
from models.attribute import AttributeModel


class AttributeRepository(Repository):
    model = AttributeModel
    def __init__(self):
        super().__init__(self.model)
