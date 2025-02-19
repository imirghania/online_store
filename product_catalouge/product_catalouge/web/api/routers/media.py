from fastapi import APIRouter, status, Response
from repository.media_repository import MediaObjectRepository
from product_catalouge.service.media_service import MediaService
from product_catalouge.service.unit_of_work import UnitOfWork
from product_catalouge.schemas.media import (
    MediaObjectIn, MediaObjectOut, MediaObjectUpdate)


router = APIRouter(prefix="/api/media", tags=["Media"])


@router.get("/", response_model=list[MediaObjectOut])
async def get_all():
    media_service = MediaService(MediaObjectRepository)
    media_objects = await media_service.get_all()
    print("="*100)
    print(f"[MEDIA]: {media_objects}")
    return [media_obj.dict() for media_obj in media_objects]


@router.get("/{id}", response_model=MediaObjectOut)
async def get_one(id:str):
    media_service = MediaService(MediaObjectRepository)
    media_object = await media_service.get_one(id)
    print("="*100)
    print(f"[MEDIA][RECORD]: {media_object.dict()}")
    return media_object.dict()


@router.post("/", response_model=MediaObjectOut, status_code=status.HTTP_201_CREATED)
async def create_media(payload:MediaObjectIn):
    async with UnitOfWork(MediaService, MediaObjectRepository) as uow:
        media_object, record = await uow.service.create(payload)
        print("="*100)
        print(f"[MEDIA][RECORD]: {record}")
        uow.track(record)
        await uow.commit()
        return media_object.dict()


@router.patch("/{id}", response_model=MediaObjectOut)
async def update_media(id:str, payload:MediaObjectUpdate):
    async with UnitOfWork(MediaService, MediaObjectRepository) as uow:
        updated_media_obj, record = await uow.service.update_one(id, payload)
        print("="*100)
        print(f"[UPDATED MEDIA]: {updated_media_obj}")
        uow.track(record)
        await uow.commit()
        return updated_media_obj.dict()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(id:str):
    async with UnitOfWork(MediaService, MediaObjectRepository) as uow:
        await uow.service.delete_one(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)