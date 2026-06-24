from urllib import request, error as url_error

def upload_file_using_presigned_url(url, file):
    req = request.Request(
        url=url,
        data=file.file.read(),
        method="PUT",
        headers={"Content-Type": file.headers.content_type or "application/octet-stream"},
    )
    try:
        with request.urlopen(req) as response:
            return {"status": response.status, "message": "File uploaded successfully."}
    except url_error.HTTPError as e:
        return {"status": 400, "message": f"HTTP Error occurred while uploading the file: {e}"}
    except url_error.URLError as e:
        return {"status": 400, "message": f"URL Error occurred while uploading the file: {e}"}