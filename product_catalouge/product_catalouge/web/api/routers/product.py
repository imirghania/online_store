from typing import Literal, Annotated
from fastapi import APIRouter, status, Response, Body
from repository.product_repository import ProductRepository
from product_catalouge.service.product_service import ProductService
from product_catalouge.service.unit_of_work import UnitOfWork
from product_catalouge.schemas.product import (
    ProductSchemaIn, ProductSchemaOut, ProductSchemaUpdate, ProductSchemaOutDetailed)


router = APIRouter(prefix="/api/product", tags=["Product"])


@router.get("/", response_model=list[ProductSchemaOut])
async def get_all():
    product_service = ProductService(ProductRepository)
    products = await product_service.get_all()
    print("="*100)
    print(f"[PRODUCTS]: {products}")
    return [product.dict() for product in products]


@router.get("/{id}", response_model=ProductSchemaOut)
async def get_one(id:str):
    product_service = ProductService(ProductRepository)
    product = await product_service.get_one(id)
    print(f"[PRODUCT][RECORD]: {product.dict()}")
    return product.dict()


@router.get("/{id}/verbose", response_model=ProductSchemaOutDetailed)
async def get_one_verbose(id:str):
    product_service = ProductService(ProductRepository)
    product = await product_service.get_one_verbose(id)
    print(f"[PRODUCT][RECORD]: {product.dict()}")
    return product.dict()


@router.post("/", response_model=ProductSchemaOut, status_code=status.HTTP_201_CREATED)
async def create_product(payload:ProductSchemaIn):
    async with UnitOfWork(ProductService, ProductRepository) as uow:
        product_type, record = await uow.service.create(payload)
        print(f"[PRODUCT SERVICE][RECORD]: {record}")
        uow.track(record)
        await uow.commit()
        return product_type.dict()


@router.patch("/{id}", response_model=ProductSchemaOut)
async def update_product(id:str, payload:ProductSchemaUpdate):
    async with UnitOfWork(ProductService, ProductRepository) as uow:
        updated_product_type, updated_record = await uow.service.update_one(id, payload)
        print(f"[UPATED TYPE]: {updated_product_type}")
        uow.track(updated_record)
        await uow.commit()
        return updated_product_type.dict()


@router.patch("/{id}/add", response_model=ProductSchemaOut)
async def add_attribute(id:str, 
                        item_id:Annotated[str, Body(embed=True)], 
                        item_type:Literal['category', 'channel', 'media']):
    async with UnitOfWork(ProductService, ProductRepository) as uow:
        updated_product_type, record = await uow.service.add_item(id, 
                                                            item_id, 
                                                            item_type)
        print(f"[UPATED PRODUCT]: {updated_product_type}")
        uow.track(record)
        await uow.commit()
        return updated_product_type.dict()


@router.patch("/{id}/remove", response_model=ProductSchemaOut)
async def remove_item(id:str, 
                        item_id:Annotated[str, Body(embed=True)], 
                        item_type:Literal['category', 'channel', 'media']):
    async with UnitOfWork(ProductService, ProductRepository) as uow:
        updated_product_type, record = await uow.service.remove_item(id, 
                                                            item_id, 
                                                            item_type)
        print(f"[UPATED PRODUCT]: {updated_product_type}")
        uow.track(record)
        await uow.commit()
        return updated_product_type.dict()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_type(id:str):
    async with UnitOfWork(ProductService, ProductRepository) as uow:
        await uow.service.delete_one(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)