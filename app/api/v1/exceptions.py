class AppError(Exception):
    pass 

class S3UploadError(AppError):
    pass 

class DatabaseInsertError(AppError):
    pass

class FileReadError(AppError):
    pass