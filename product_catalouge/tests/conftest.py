from contextlib import asynccontextmanager
import pytest
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import pytest_asyncio
from product_catalouge.core.config import settings
from product_catalouge.lib.models_loader import get_beanie_models
from product_catalouge.lib.db_initializer import init_db
from product_catalouge.web.api.routers import (
    attribute, category, product_type, media, product)


routers = [attribute, category, product_type, media, product]

@pytest_asyncio.fixture(autouse=True)
async def testdb():
    db_client = AsyncIOMotorClient(settings.db_uri)
    try:
        # Verify the connection
        await db_client.server_info()
        print("[TEST DB CONNECTION] MongoDB connection successful.")
    except Exception as e:
        print(f"[TEST DB CONNECTION] MongoDB connection failed: {e}")
        raise
    await init_beanie(database=db_client.get_database(name=settings.test_db_name),
                            document_models=get_beanie_models())
    print("[TEST DB INITIALIZATION] Beanie initialization complete.")
    yield db_client
    await db_client.drop_database(settings.test_db_name)
    print("[TEST DB TEARDOWN] Test database dropped.")


@pytest_asyncio.fixture()
async def test_lifespan():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await init_db(settings.db_uri, settings.test_db_name)  
        yield  
    return lifespan


@pytest.fixture(autouse=True)
def test_app(test_lifespan):
    app = FastAPI(
        title="Product Catalogue Service (Test)",
        docs_url="/api/docs",
        openapi_url="/api/openapi",
        lifespan=test_lifespan,
    )
    for router in routers:
        app.include_router(router.router)
    return app