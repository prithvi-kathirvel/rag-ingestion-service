from sqlalchemy import create_engine, text
from app.core.config import get_config
from uuid import UUID
from datetime import datetime

config = get_config()

def _serialize(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value
class Database:
    def __init__(self,dialect:str,host:str,port:str,user:str,password:str,database:str,driver:str = None,exclude_tables:list[str] = None,**kwargs):
        self.dialect = dialect  
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.driver = driver
        self.exclude_tables = []
     


    def get_connection_string(self):
            driver_part = f"+{self.driver}" if self.driver else ""
            return f"{self.dialect}{driver_part}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        

    def create_engine(self):
            connection_string = self.get_connection_string()
            return create_engine(connection_string, pool_pre_ping=True, future=True)
    

    def execute_query(self, query:str,params:dict = None):
        engine = self.create_engine()
        with engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            rows = result.mappings().all()
            results = [{key: _serialize(value) for key, value in row.items()} for row in rows]
            return results
    
    async def execute_async_query(self, query:str,params:dict = None):
        from sqlalchemy.ext.asyncio import create_async_engine
        connection_string = self.get_connection_string()
        async_engine = create_async_engine(connection_string, pool_pre_ping=True, future=True)
        async with async_engine.connect() as connection:
            result = await connection.execute(text(query), params or {})
            rows = result.mappings().all()
            results = [{key: _serialize(value) for key, value in row.items()} for row in rows]
            return results

