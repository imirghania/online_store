from product_catalouge.repository.base_repository import Repository
from .domain import Attribute
from .base_service import Service


class AttributeService(Service):
    __model_label__ = "Attribute"
    def __init__(self, repository: Repository):
        super().__init__(repository, Attribute)