from fastapi import Request
import asyncpg
from httpx import request
from app.db.database import Database
from app.services.metadata_service import MetaDataExtractor


async def get_db(request: Request) -> Database:
    database = getattr(request.app.state, "database", None)
    if database is None:
        raise Exception("Database not initialized")
    return database

async def get_metadata_extractor(request: Request) -> MetaDataExtractor:
    metadata_extractor = getattr(request.app.state, "metadata_extractor", None)
    if metadata_extractor is None:
        raise Exception("MetaDataExtractor not initialized")
    return metadata_extractor