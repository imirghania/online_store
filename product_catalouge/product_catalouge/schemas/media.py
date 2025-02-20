from typing import Optional
from pydantic import BaseModel, HttpUrl, field_validator


class Image(BaseModel):
    url: HttpUrl
    alt: Optional[str] = None
    width: int
    height: int
    
    @field_validator("url", mode="after")
    def convert_url_to_str(cls, value):
        return str(value)


class ImageUpdate(Image):
    url: Optional[HttpUrl] = None
    width: Optional[int] = None
    height: Optional[int] = None


class MediaObject(BaseModel):
    title: str
    image: Image
    thumbnail: Optional[Image] = None

    def model_post_init(self, __context) -> None:
        if (self.thumbnail is not None) and self.image.alt is not None:
            self.thumbnail.alt = (self.image.alt + " [thumbnail]"
                                if self.image.alt is not None
                                else "[thumbnail]")
    def dict(self):
        return self.model_dump()


class MediaObjectIn(MediaObject):
    ...


class MediaObjectOut(MediaObject):
    id: str


class MediaObjectUpdate(MediaObject):
    title: Optional[str] = None
    image: Optional[ImageUpdate] = None
    thumbnail: Optional[ImageUpdate] = None

    def model_post_init(self, __context) -> None:
        if self.image is not None and self.thumbnail is not None:
            self.thumbnail.alt = self.image.alt + " [thumbnail]"

    def dict(self):
        return self.model_dump(exclude_unset=True)






def main():
    image_payload = {
        "url": "url",
        "alt": "image description",
        "width": 250,
        "height": 250
    }
    image = Image(**image_payload)
    media = MediaObject(title="Media object title", image=image)
    
    print(f"[MEDIA OBJECT][INSTANCE]: {media}")
    print(f"[MEDIA OBJECT][DICT]: {media.dict()}")

if __name__ == "__main__":
    main()