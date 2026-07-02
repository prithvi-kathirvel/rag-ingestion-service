import json
from typing import Literal

import boto3
from io import BytesIO
import mimetypes
from pathlib import Path
import uuid

from app.core.logging import logger
from app.core.config import get_config
from app.api.v1.exceptions import DatabaseInsertError, FileReadError, S3UploadError
from app.schema.ingest import DocumentCreate
from app.utils.helper import calculate_hash
from app.query.queries import INSERT_DOCUMENT
from app.services.parser_service import ParserService
from app.services.metadata_service import MetaDataExtractor


UploadType = Literal["raw", "processed", "both"]


class S3Service:
    def __init__(self, client):
        self.client = client

    def upload_file(self, file, bucket_name, key, extra_args):
        logger.info(f"Uploading file to S3 bucket: {bucket_name}, key: {key}")
        try:
            self.client.upload_fileobj(file, bucket_name, key, ExtraArgs=extra_args)
            logger.info(f"File uploaded successfully to S3 bucket: {bucket_name}, key: {key}")
        except Exception as e:
            logger.error(f"Error uploading file to S3: {str(e)}")
            raise S3UploadError("Error uploading file to S3") from e


class IngestionService:
    def __init__(self, db, s3_client, metadata_extractor: MetaDataExtractor):
        self.db = db
        self.s3 = S3Service(s3_client)
        self.config = get_config()
        self.metadata_extractor = metadata_extractor

    def _build_key(self, folder_path: str, document_id: str, suffix: str) -> str:
        return f"{folder_path}/{document_id}{suffix}"

    async def upload_file(self, file, bucket_name: str, user: dict, upload_type: UploadType = "raw"):
        file_content = await file.read()
        document_id = str(uuid.uuid4())
        suffix = Path(file.filename or "").suffix
        checksum = await calculate_hash(file, algorithm="sha256")
        content_type = file.content_type or mimetypes.guess_type(file.filename or "")[0] or "application/octet-stream"
        user_id = user["user_id"]

        raw_root = self.config.S3_RAW_ROOT_FOLDER
        processed_root = self.config.S3_PROCESSED_ROOT_FOLDER

        try:
            primary_key = None

            if upload_type in ("raw", "both"):
                raw_key = self._build_key(f"{raw_root}/{user_id}", document_id, suffix)
                self.s3.upload_file(BytesIO(file_content), bucket_name, raw_key, extra_args={"ContentType": content_type})
                primary_key = raw_key

            if upload_type in ("processed", "both"):
                parser = ParserService(api_key=self.config.LLAMA_CLOUD_API_KEY, metadata_extractor=self.metadata_extractor)
                chunks_with_metadata = await parser.parse_file(file_content, file.filename)
                processed_key = self._build_key(f"{processed_root}/{user_id}", document_id, ".json")
                self.s3.upload_file(
                    BytesIO(json.dumps(chunks_with_metadata).encode("utf-8")),
                    bucket_name,
                    processed_key,
                    extra_args={"ContentType": "application/json"},
                )
                if primary_key is None:
                    primary_key = processed_key

            document = DocumentCreate(
                id=document_id,
                original_filename=file.filename,
                stored_filename=primary_key,
                mime_type=content_type,
                file_size=file.size,
                s3_bucket=bucket_name,
                s3_key=primary_key,
                checksum=checksum,
                uploaded_by=user_id if user else uuid.UUID("00000000-0000-0000-0000-000000000001"),
                status="UPLOADED",
                current_version=1,
                deleted=False,
            )
            logger.info(f"Document created: {document.model_dump(mode='json')}")
            await self.db.execute_async_query(INSERT_DOCUMENT, document.model_dump(mode="json"))
            logger.info(f"Document inserted into database: {document_id}")

            return {"message": "File Uploaded Successfully", "status": 200}

        except S3UploadError:
            raise
        except OSError as e:
            logger.error(f"Error while reading file: {str(e)}")
            raise FileReadError("Error while reading uploaded file") from e
        except Exception as e:
            logger.error(f"Error while uploading file: {str(e)}")
            raise DatabaseInsertError("Error while uploading file metadata") from e


