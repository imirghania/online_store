from typing import Annotated
from beanie import Document, Indexed
from schemas.media import Image


__all__ = ("MediaObjectModel",)


class MediaObjectModel(Document):
    title: str
    slug: Annotated[str, Indexed(unique=True)]
    image: Image
    thumbnail: Image

    class Settings:
        name = "media_objects"
        use_state_management = True

    def dict(self):
        return {
            "id": self.id,
            "title": self.title, 
            "image": self.image.dump_model(), 
            "thumbnail": self.thumbnail.dump_model(), 
        }