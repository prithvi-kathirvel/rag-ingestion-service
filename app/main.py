from contextlib import asynccontextmanager
from fastapi import FastAPI
from uvicorn import logging
from app.api.v1.api import router
from app.db.database import Database
from app.core.config import get_config
from app.core.logging import setup_logging,logger,logging_middleware
from app.services.metadata_service import MetaDataExtractor

settings = get_config()
setup_logging(environment=settings.ENVIRONMENT)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application") 
    logger.info("Connecting to database")
    database = Database(
        dialect="postgresql",
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        database=settings.DATABASE_NAME,
        driver="asyncpg"
        
    )
    app.state.database = database

    app.state.metadata_extractor = MetaDataExtractor.from_pretrained(
        model_name=settings.GLINER2_MODEL,
        threshold=settings.GLINER2_MODEL_THRESHOLD,
    )
    yield
    logger.info("Shutting down application")

app = FastAPI(
    title="RAG Service",
    description="A template for building FastAPI applications",
    version="1.0.0",
    lifespan=lifespan
)
logging_middleware(app)
app.include_router(router, prefix="/api/v1")