from fastapi import APIRouter
from product_catalouge.service.attributes_service import AttributeService
from repository.unit_of_work import UnitOfWork
from repository.attribute_repository import AttributeRepository


router = APIRouter()


@router.get("/attributes/", tags=["attributes"])
async def get_all_attributes():
    with UnitOfWork(AttributeRepository) as uow:
        attribute_service = AttributeService(uow.repository)
        attribute_service.get_all()


@router.get("/attributes/{id}", tags=["attributes"])
async def get_one(id:str):
    with UnitOfWork(AttributeRepository) as uow:
        attribute_service = AttributeService(uow.repository)
        attribute = attribute_service.get_by_id(id)


@router.post("/attributes/", tags=["attributes"])
async def create_attribute(payload):
    with UnitOfWork(AttributeRepository) as uow:
        attribute_service = AttributeService(uow.repository)
        attribute = attribute_service.create(payload)
        uow.commit()
        return attribute.dict()