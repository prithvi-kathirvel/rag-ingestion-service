import hashlib
from app.utils.metadata import METADATA

async def calculate_hash(upload_file, algorithm="sha256"):
    hasher = hashlib.new(algorithm)

    while chunk := await upload_file.read(1024 * 1024):
        hasher.update(chunk)

    await upload_file.seek(0)

    return hasher.hexdigest()

def get_gliner2_structure_format(metadata=METADATA):
    if not metadata:
        return {"response": []}

    structure_format = []

    for item in metadata:
        if not isinstance(item, dict):
            continue

        name = item.get("name")
        type_ = item.get("type")
        description = item.get("description")

        if not all([name, type_, description]):
            continue

        structure_format.append(f"{name}::{type_}::{description}")

    return {"response": structure_format}