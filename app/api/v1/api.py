import asyncpg
from fastapi import APIRouter, Depends
from typing import Annotated
from app.core.config import Config,get_config
from app.api.v1.deps import get_db
from app.api.v1.ingest import ingestion_router
from app.core.middleware import get_current_user


router = APIRouter(dependencies=[Depends(get_current_user)], prefix="/api/v1") 


router.include_router(ingestion_router)


@router.get("/health")
async def health_check(config: Annotated[Config, Depends(get_config)]):
    return {"status": "ok", "version": config.VERSION}