from typing import Any
from beanie import PydanticObjectId
from exceptions.database_exceptions import (DuplicateRecordError,
                                            InvalidInputError, RecordNotFound)
from models.media import MediaObjectModel
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError
from .base_repository import Repository



class MediaObjectRepository(Repository):
    model = MediaObjectModel
    def __init__(self):
        super().__init__(self.model)


    async def update_one(self, id:PydanticObjectId, payload:dict[str, Any]):
        try:
            media = await self.get_one(id)
            print("="*100)
            print(f"[MEDIA REPOSITORY][DOCUMENT][BASE]: {media}")
            if not media:
                raise RecordNotFound

            if "media" in payload:
                payload["image"] = media.image.model_copy(**payload["image"])

            if "thumbnail" in payload:
                payload["thumbnail"] = media.thumbnail.model_copy(**payload["thumbnail"])
            
            for key, value in payload.items():
                setattr(media, key, value)
            print("="*100)
            print(f"[MEDIA REPOSITORY][DOCUMENT][UPDATED]: {media}")
            
            return media
        except ValidationError as e:
            raise InvalidInputError
        except DuplicateKeyError as e:
            raise DuplicateRecordError