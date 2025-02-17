from typing import Optional
from pydantic import BaseModel, Field


class Image(BaseModel):
    url: str
    alt: Optional[str] = None
    width: int
    height: int


class MediaObject(BaseModel):
    title: str
    image: Image
    thumbnail: Optional[Image] = None

    def model_post_init(self, __context) -> None:
        if self.thumbnail is not None:
            self.thumbnail.alt = self.image.alt + " [thumbnail]"


class MediaObjectIn(MediaObject):
    ...


class MediaObjectOut(MediaObject):
    title: Optional[str] = None
    image: Optional[Image] = None


class Media(BaseModel):
    items: Optional[list[str]] = Field(default_factory=list)
    main_media: Optional[str] = None