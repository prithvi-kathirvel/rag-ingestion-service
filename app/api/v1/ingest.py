from fastapi import APIRouter,UploadFile, File
import boto3
from app.core import config
from app.core.config import get_config
from app.services.ingestion_service import upload_file_using_presigned_url
import uuid


config = get_config()


ingestion_router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@ingestion_router.post("/upload")
async def upload_file_into_s3(file: UploadFile = File(...)):

    s3 = boto3.client('s3')
    bucket_name = config.AWS_BUCKET_NAME
    folder_name = config.AWS_DEFAULT_FOLDER
    uuid_str = str(uuid.uuid4())
    key = f"{folder_name}/{uuid_str}"

    try:
        s3.upload_fileobj(file.file, bucket_name, key,ExtraArgs={"ContentType": file.content_type})
        return {"message":"File Uploaded Successfully","status":200}

    except Exception as e:
        return {"message":"Error while Uploading File","error":str(e)}
    




@ingestion_router.get("/get-files")
async def get_files_from_s3():
    s3 = boto3.client('s3') 
    bucket_name = config.AWS_BUCKET_NAME
    
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix='raw/')
    # return response
    
    final_response = [
        {
            "file": obj['Key'],
            "last_modified": obj['LastModified'],
            "size": obj['Size']
        }
        for obj in response.get('Contents', [])
        if not obj['Key'].endswith('/')
    ]
    
    return final_response




    return {"message": "Get files from S3 endpoint"}

    