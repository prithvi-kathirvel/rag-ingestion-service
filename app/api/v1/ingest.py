import boto3
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from app.api.v1.exceptions import DatabaseInsertError, FileReadError, S3UploadError
from app.core.config import get_config
from app.api.v1.deps import get_db, get_metadata_extractor
from app.core.middleware import get_current_user
from app.services.ingestion_service import IngestionService, UploadType
from app.core.logging import logger
from app.services.metadata_service import MetaDataExtractor



config = get_config()


ingestion_router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@ingestion_router.post("/upload")
async def upload_file_into_s3( file: UploadFile = File(...), upload_type: UploadType = Query(default="raw"), db=Depends(get_db), user=Depends(get_current_user),metadata_extractor: MetaDataExtractor = Depends(get_metadata_extractor)):
    s3_client = boto3.client('s3')
    ingestion_service = IngestionService(db, s3_client, metadata_extractor=metadata_extractor)
    bucket_name = config.AWS_BUCKET_NAME
    user_id = user["user_id"]
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required for file upload")

    try:
        await ingestion_service.upload_file(file, bucket_name, user, upload_type)

    except FileReadError as e:
        logger.error(f"Error reading file: {str(e)}")
        raise HTTPException(status_code=400, detail="Error reading file")
    except S3UploadError as e:
        logger.error(f"Error uploading file to S3: {str(e)}")
        raise HTTPException(status_code=502, detail="Error uploading file to S3")
    except DatabaseInsertError as e:
        logger.error(f"Error inserting file metadata into database: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inserting file metadata into database")
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error uploading file")


    




@ingestion_router.get("/get-files")
async def get_files_from_s3():
    s3 = boto3.client('s3') 
    bucket_name = config.AWS_BUCKET_NAME
    
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix='raw/')
    final_response = [
        {
            "filename": obj['Key'].split('/')[-1],
            "file_path": obj['Key'],
            "last_modified": obj['LastModified'],
            "size": obj['Size']
        }
        for obj in response.get('Contents', [])
        if not obj['Key'].endswith('/')
    ]
    return final_response

@ingestion_router.delete("/delete-file")
async def delete_file_from_s3(file_path: str):
    s3 = boto3.client('s3') 
    bucket_name = config.AWS_BUCKET_NAME
    filename = file_path.split('/')[-1]
    
    try:
        s3.delete_object(Bucket=bucket_name, Key=file_path)
        return {"message": f"File {filename} deleted successfully from S3."}
    except Exception as e:
        logger.error(f"Error deleting file from S3: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting file from S3")

    