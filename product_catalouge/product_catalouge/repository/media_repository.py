from base_repository import Repository
from models import MediaObjectModel, MediaModel
from service.domain import MediaObject


class MediaObjectRepository(Repository):
    async def __init__(self):
        super().__init__(MediaObjectModel)
    
    async def create(self, payload):
        record = await self.model(**payload)
        return MediaObject(**record.dict())