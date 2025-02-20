from .base_repository import Repository
from models.variant import VariantModel


class VariantRepository(Repository):
    model = VariantModel
    def __init__(self):
        super().__init__(self.model)