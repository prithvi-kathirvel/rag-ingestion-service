from pydantic import BaseModel, Field
from typing import Optional 


class DatabaseConfigurationSchema(BaseModel):
    dialect: str = Field(..., description="The database dialect (e.g., 'postgresql', 'mysql', 'sqlite').")
    host: str = Field(..., description="The database host.")
    port: int = Field(..., description="The database port.")
    user: str = Field(..., description="The database user.")
    password: str = Field(..., description="The database password.")
    database: str = Field(..., description="The database name.")