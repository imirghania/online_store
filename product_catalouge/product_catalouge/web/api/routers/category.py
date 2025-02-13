from fastapi import APIRouter, status, Response
from repository.category_repository import CategoryRepository
from product_catalouge.service.categories_service import CategoryService
from product_catalouge.service.unit_of_work import UnitOfWork
from product_catalouge.schemas.category import (
    CategorySchemaIn, CategorySchemaOut, CategoryUpdateSchema)


router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/", response_model=list[CategorySchemaOut])
async def get_all():
    category_service = CategoryService(CategoryRepository)
    categories = await category_service.get_all()
    print(f"[ATTRIBUTEs]: {categories}")
    return [attr.dict() for attr in categories]


@router.get("/{id}", response_model=CategorySchemaOut)
async def get_one(id:str):
    category_service = CategoryService(CategoryRepository)
    category = await category_service.get_one(id)
    print(f"[CATEGORY][RECORD]: {category.dict()}")
    return category.dict()


@router.post("/", response_model=CategorySchemaOut, status_code=status.HTTP_201_CREATED)
async def create_category(payload:CategorySchemaIn):
    async with UnitOfWork(CategoryService, CategoryRepository) as uow:
        category, record, parent = await uow.service.create(payload)
        print(f"[CATEGORY SERVICE][RECORD]: {record}")
        uow.track(record)
        if parent is not None:
            uow.track(parent)
        await uow.commit()
        return category.dict()


@router.patch("/{id}", response_model=CategorySchemaOut)
async def update_category(id:str, payload:CategoryUpdateSchema):
    async with UnitOfWork(CategoryService, CategoryRepository) as uow:
        updated_category, updated_record = await uow.service.update_one(id, payload)
        print(f"[UPATED Attribute]: {updated_category}")
        uow.track(updated_record)
        await uow.commit()
        return updated_category.dict()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id:str):
    async with UnitOfWork(CategoryService, CategoryRepository) as uow:
        objects = await uow.service.delete_one(id)
        uow.track(*objects)
        await uow.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
