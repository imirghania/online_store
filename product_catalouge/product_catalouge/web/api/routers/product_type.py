from typing import Literal
from fastapi import APIRouter, status, Response
from repository.product_type_repository import ProductTypeRepository
from product_catalouge.service.product_type_service import ProductTypeService
from product_catalouge.service.unit_of_work import UnitOfWork
from product_catalouge.schemas.product_type import (
    ProductTypeSchemaIn, ProductTypeSchemaOut, ProductTypeSchemaUpdate, 
    ProductTypeSchemaOutDetailed)


router = APIRouter(prefix="/api/product-types", tags=["Product Types"])


@router.get("/", response_model=list[ProductTypeSchemaOut])
async def get_all():
    product_type_service = ProductTypeService(ProductTypeRepository)
    product_types = await product_type_service.get_all()
    print("="*100)
    print(f"[PRODUCT TYPES]: {product_types}")
    return [product_type.dict() for product_type in product_types]


@router.get("/{id}", response_model=ProductTypeSchemaOut)
async def get_one(id:str):
    product_type_service = ProductTypeService(ProductTypeRepository)
    product_type = await product_type_service.get_one(id)
    print(f"[PRODUCT TYPE][RECORD]: {product_type.dict()}")
    return product_type.dict()


@router.get("/{id}/verbose", response_model=ProductTypeSchemaOutDetailed)
async def get_one_with_details(id:str):
    product_type_service = ProductTypeService(ProductTypeRepository)
    product_type = await product_type_service.get_one_verbose(id)
    print(f"[PRODUCT TYPE][RECORD]: {product_type.dict()}")
    return product_type.dict()


@router.post("/", response_model=ProductTypeSchemaOut, status_code=status.HTTP_201_CREATED)
async def create_product_type(payload:ProductTypeSchemaIn):
    async with UnitOfWork(ProductTypeService, ProductTypeRepository) as uow:
        product_type, record = await uow.service.create(payload)
        print(f"[PRODUCT TYPE SERVICE][RECORD]: {record}")
        uow.track(record)
        await uow.commit()
        return product_type.dict()


@router.patch("/{id}", response_model=ProductTypeSchemaOut)
async def update_product_type(id:str, payload:ProductTypeSchemaUpdate):
    async with UnitOfWork(ProductTypeService, ProductTypeRepository) as uow:
        updated_product_type, updated_record = await uow.service.update_one(id, payload)
        print(f"[UPATED PRODUCT TYPE]: {updated_product_type}")
        uow.track(updated_record)
        await uow.commit()
        return updated_product_type.dict()


@router.patch("/{id}/add-attribute", response_model=ProductTypeSchemaOut)
async def add_attribute(id:str, 
                        attribute_id:str, 
                        attribute_type:Literal["general", "variant"]):
    async with UnitOfWork(ProductTypeService, ProductTypeRepository) as uow:
        updated_product_type, record = await uow.service.add_attribute(id, 
                                                            attribute_id, 
                                                            attribute_type)
        print(f"[UPATED PRODUCT TYPE]: {updated_product_type}")
        uow.track(record)
        await uow.commit()
        return updated_product_type.dict()


@router.patch("/{id}/remove-attribute", response_model=ProductTypeSchemaOut)
async def add_attribute(id:str, 
                        attribute_id:str, 
                        attribute_type:Literal["general", "variant"]):
    async with UnitOfWork(ProductTypeService, ProductTypeRepository) as uow:
        updated_product_type, record = await uow.service.remove_attribute(id, 
                                                            attribute_id, 
                                                            attribute_type)
        print(f"[UPATED PRODUCT TYPE]: {updated_product_type}")
        uow.track(record)
        await uow.commit()
        return updated_product_type.dict()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_type(id:str):
    async with UnitOfWork(ProductTypeService, ProductTypeRepository) as uow:
        await uow.service.delete_one(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)