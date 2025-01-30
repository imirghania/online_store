from contextlib import asynccontextmanager
from fastapi import FastAPI
from product_catalouge.core.config import settings
from product_catalouge.lib.db_initializer import init_db
from .routers import attribute


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(settings.db_uri, settings.db_name)
    yield

app = FastAPI(docs_url="/api/docs", 
            openapi_url="/api", 
            lifespan=lifespan)

app.include_router(attribute.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}