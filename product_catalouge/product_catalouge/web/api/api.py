from contextlib import asynccontextmanager
from fastapi import FastAPI
from product_catalouge.core.config import settings
from product_catalouge.lib.db_initializer import init_db
from .routers import attribute, category, product_type, media, product


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(settings.db_uri, settings.db_name)
    yield

app = FastAPI(title="Product Catalouge Service",
            docs_url="/api/docs", 
            openapi_url="/api/openapi", 
            lifespan=lifespan)

app.include_router(attribute.router)
app.include_router(category.router)
app.include_router(product_type.router)
app.include_router(media.router)
app.include_router(product.router)

@app.get("/")
async def root():
    return {"message": "Hello, This is a product catalog service API"}