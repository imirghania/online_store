from typing import Annotated
from beanie import Document, Indexed
from schemas.media import MediaObject


__all__ = ("MediaObjectModel",)


class MediaObjectModel(MediaObject, Document):
    title: Annotated[str, Indexed(unique=True)]

    class Settings:
        name = "media_objects"
        use_state_management = True