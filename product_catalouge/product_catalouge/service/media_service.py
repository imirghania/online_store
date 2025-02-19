from product_catalouge.repository.media_repository import(
    MediaObjectRepository)
from .base_service import Service
from .domain import Media



class MediaService(Service):
    model_label = "Media"
    def __init__(self, repository: MediaObjectRepository):
        super().__init__(repository, Media)