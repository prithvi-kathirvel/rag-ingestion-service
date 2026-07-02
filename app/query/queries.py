INSERT_DOCUMENT = """  
INSERT INTO document (id, original_filename, stored_filename, mime_type, file_size, s3_bucket, s3_key, checksum, uploaded_by, status, current_version, deleted)
VALUES (:id, :original_filename, :stored_filename, :mime_type, :file_size, :s3_bucket, :s3_key, :checksum, :uploaded_by, :status, :current_version, :deleted)
"""