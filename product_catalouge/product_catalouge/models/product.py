from models.category import CategoryModel, Annotated, Optional, Document, Indexed, Link
from models.product_type import ProductTypeModel, Field
from schemas.main import Media


__all__ = ("ProductModel",)


class ProductModel(Document):
    name: str
    slug: Annotated[str, Indexed(unique=True)]
    product_type: Link[ProductTypeModel]
    categories: Optional[list[Link[CategoryModel]]] = Field(default_factory=list)
    channels: Optional[list[str]] = Field(default_factory=list)
    media: Optional[Media] = None

    class Settings:
        name = "products"
        use_state_management = True

    def dict(self):
        categories = [category.dict() for category in self.categories]
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug, 
            "product_type": self.product_type.dict(), 
            "categories": categories, 
            "channels": self.channels, 
            "media": self.media.dump_model(), 
        }


