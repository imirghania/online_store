from models.category import CategoryModel
from .base_repository import Repository


class CategoryRepository(Repository):
    model = CategoryModel
    def __init__(self):
        super().__init__(self.model)

    async def create(self, payload:dict):
        record = await super().create(payload)
        await record.fetch_all_links()
        print(f"[CATEGORY REPOSITORY][RECORD]: {record}")
        return record