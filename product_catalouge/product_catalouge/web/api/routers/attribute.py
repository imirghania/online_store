from fastapi import APIRouter, status
from repository.attribute_repository import AttributeRepository
from product_catalouge.service.attributes_service import AttributeService
from product_catalouge.service.unit_of_work import UnitOfWork
from product_catalouge.schemas.attribute import AttributeSchema


router = APIRouter()


@router.get("/attributes/", tags=["attributes"])
async def get_all():
    attribute_service = AttributeService(AttributeRepository)
    attributes = await attribute_service.get_all()
    print(f"[ATTRIBUTEs]: {attributes}")
    return [attr.dict() for attr in attributes]


@router.get("/attributes/{id}", tags=["attributes"])
async def get_one(id:str):
    attribute_service = AttributeService(AttributeRepository)
    attribute = await attribute_service.get_by_id(id)
    print(f"[ATTRIBUTE]: {attribute.dict()}")
    return attribute.dict()


@router.post("/attributes/", tags=["attributes"])
async def create_attribute(payload: AttributeSchema):
    async with UnitOfWork(AttributeService, AttributeRepository) as uow:
        attribute = await uow.service.create(payload)
        uow.track(attribute)
        uow.commit()
        return attribute.dict()


@router.delete("/attributes/{id}", tags=["attributes"], 
            status_code=status.HTTP_204_NO_CONTENT)
async def delete_attribute(id:str):
    async with UnitOfWork(AttributeService, AttributeRepository) as uow:
        attribute = await uow.service.delete_by_id(id)
        uow.track(attribute)
        await uow.commit()
