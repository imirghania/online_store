from fastapi import APIRouter, status, Response
from repository.attribute_repository import AttributeRepository
from product_catalouge.service.attributes_service import AttributeService
from product_catalouge.service.unit_of_work import UnitOfWork
from product_catalouge.schemas.attribute import (
    AttributeSchema, AttributeSchemaOut, AttributeUpdateSchema)


router = APIRouter(prefix="/api/attributes", tags=["attributes"])


@router.get("/", response_model=list[AttributeSchemaOut])
async def get_all():
    attribute_service = AttributeService(AttributeRepository)
    attributes = await attribute_service.get_all()
    print(f"[ATTRIBUTES]: {attributes}")
    return [attr.dict() for attr in attributes]


@router.get("/{id}", response_model=AttributeSchemaOut)
async def get_one(id:str):
    attribute_service = AttributeService(AttributeRepository)
    attribute = await attribute_service.get_one(id)
    print(f"[ATTRIBUTE]: {attribute.dict()}")
    return attribute.dict()


@router.post("/", response_model=AttributeSchemaOut, status_code=status.HTTP_201_CREATED)
async def create_attribute(payload:AttributeSchema):
    async with UnitOfWork(AttributeService, AttributeRepository) as uow:
        attribute, record = await uow.service.create(payload)
        uow.track(record)
        await uow.commit()
        return attribute.dict()


@router.patch("/{id}", response_model=AttributeSchemaOut)
async def update_attribute(id:str, payload:AttributeUpdateSchema):
    async with UnitOfWork(AttributeService, AttributeRepository) as uow:
        updated_attribute, updated_record = await uow.service.update_one(id, payload)
        print(f"[UPATED Attribute]: {updated_attribute}")
        uow.track(updated_record)
        await uow.commit()
        return updated_attribute.dict()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attribute(id:str):
    async with UnitOfWork(AttributeService, AttributeRepository) as uow:
        attribute = await uow.service.delete_one(id)
        print(f"[DELETED][DOCUMENT]: {attribute}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
