from fastapi import APIRouter
from product_catalouge.service.attributes_service import AttributeService
from product_catalouge.service.unit_of_work import UnitOfWork
from repository.attribute_repository import AttributeRepository


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
async def create_attribute(payload: AttributeRepository.model):
    async with UnitOfWork(AttributeService, AttributeRepository) as uow:
        attribute = await uow.service.create(payload)
        uow.track(attribute)
        uow.commit()
        return attribute.dict()