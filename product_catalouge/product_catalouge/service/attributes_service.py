from product_catalouge.repository.attribute_repository import AttributeRepository
from .domain import Attribute
from .base_service import Service


class AttributeService(Service):
    __model_label__ = "Attribute"
    def __init__(self, repository: AttributeRepository):
        super().__init__(repository, Attribute)


attribute_service = AttributeService(AttributeRepository)