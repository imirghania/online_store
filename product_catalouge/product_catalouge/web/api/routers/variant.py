from typing import Literal, Annotated
from fastapi import APIRouter, status, Response, Body
from repository.variant_repository import VariantRepository
from product_catalouge.service.variant_service import VariantService
from product_catalouge.service.unit_of_work import UnitOfWork
from product_catalouge.schemas.variant import (
    VariantSchemaIn, VariantSchemaOut, VariantSchemaUpdate, VariantSchemaOutDetailed)


router = APIRouter(prefix="/api/variant", tags=["Variant"])


@router.get("/", response_model=list[VariantSchemaOut])
async def get_all():
    variant_service = VariantService(VariantRepository)
    variants = await variant_service.get_all()
    print("="*100)
    print(f"[VARIANTS]: {variants}")
    return [variant.dict() for variant in variants]


@router.get("/{id}", response_model=VariantSchemaOut)
async def get_one(id:str):
    variant_service = VariantService(VariantRepository)
    variant = await variant_service.get_one(id)
    print(f"[VARIANT][RECORD]: {variant.dict()}")
    return variant.dict()


@router.post("/", response_model=VariantSchemaOut, status_code=status.HTTP_201_CREATED)
async def create_variant(payload:VariantSchemaIn):
    async with UnitOfWork(VariantService, VariantRepository) as uow:
        variant, record = await uow.service.create(payload)
        print(f"[VARIANT SERVICE][RECORD]: {record}")
        uow.track(record)
        await uow.commit()
        return variant.dict()


@router.get("/{id}/verbose", 
            response_model=VariantSchemaOutDetailed,
            response_model_exclude_none=True)
async def get_one_verbose(id:str):
    variant_service = VariantService(VariantRepository)
    variant = await variant_service.get_one_verbose(id)
    print(f"[VARIANT][RECORD]: {variant.dict()}")
    return variant.dict()


# @router.patch("/{id}", response_model=VariantSchemaOut)
# async def update_product(id:str, payload:VariantSchemaUpdate):
#     async with UnitOfWork(VariantService, VariantRepository) as uow:
#         updated_variant, updated_record = await uow.service.update_one(id, payload)
#         print(f"[UPATED VARIANT]: {updated_variant}")
#         uow.track(updated_record)
#         await uow.commit()
#         return updated_variant.dict()


# @router.patch("/{id}/add", response_model=VariantSchemaOut)
# async def add_attribute(id:str, 
#                         item_id:Annotated[str, Body(embed=True)], 
#                         item_type:Literal['media', 'stock', 'price']):
#     async with UnitOfWork(VariantService, VariantRepository) as uow:
#         updated_product_type, record = await uow.service.add_item(id, 
#                                                             item_id, 
#                                                             item_type)
#         print(f"[UPATED VARIANT]: {updated_product_type}")
#         uow.track(record)
#         await uow.commit()
#         return updated_product_type.dict()


@router.patch("/{id}/remove", response_model=VariantSchemaOut)
async def remove_item(id:str, 
                        item_id:Annotated[str, Body(embed=True)], 
                        item_type:Literal['category', 'channel', 'media']):
    async with UnitOfWork(VariantService, VariantRepository) as uow:
        updated_product_type, record = await uow.service.remove_item(id, 
                                                            item_id, 
                                                            item_type)
        print(f"[UPATED VARIANT]: {updated_product_type}")
        uow.track(record)
        await uow.commit()
        return updated_product_type.dict()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_type(id:str):
    async with UnitOfWork(VariantService, VariantRepository) as uow:
        await uow.service.delete_one(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)