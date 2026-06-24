from fastapi import Request
import asyncpg
from app.db.database import Database


async def get_db(request: Request) -> Database:
    database = getattr(request.app.state, "database", None)
    if database is None:
        raise Exception("Database not initialized")
    return database