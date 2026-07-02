from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )
    id: UUID
    original_filename: str = Field(min_length=1, max_length=255)
    stored_filename: str = Field(min_length=1, max_length=255)
    mime_type: str = Field(min_length=1, max_length=100)
    file_size: int = Field(gt=0,description="File size in bytes")
    s3_bucket: str = Field(min_length=3, max_length=63)
    s3_key: str = Field(min_length=1, max_length=1024)
    checksum: str = Field(min_length=32, max_length=128)
    uploaded_by: UUID
    status: str = Field(pattern="^(UPLOADING|UPLOADED|PROCESSING|PROCESSED|FAILED|DELETED)$")
    current_version: int = Field(ge=1)
    metadata: dict[str, Any] = Field(default_factory=dict)
    deleted: bool = False