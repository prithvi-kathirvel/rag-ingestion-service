from pathlib import Path
import json
import sys

# Ensure project root is importable when this file is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from llama_cloud import LlamaCloud
from app.core.config import get_config


def _to_jsonable(value):
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    if hasattr(value, "model_dump"):
        return _to_jsonable(value.model_dump())
    if hasattr(value, "to_dict"):
        return _to_jsonable(value.to_dict())
    return str(value)

config = get_config()

client = LlamaCloud(api_key=config.LLAMA_CLOUD_API_KEY)

# Upload
file_obj = client.files.create(file="./document.pdf", purpose="parse")

# Submit + poll + get (parsing.parse wraps create / wait_for_completion / get)
# Raises on FAILED or CANCELLED. Tune polling_interval=, timeout= if needed.
result = client.parsing.parse(
    file_id=file_obj.id,
    # The parsing tier. Options: fast, cost_effective, agentic, agentic_plus,
    tier="cost_effective",
    # The version of the parsing tier to use. Use 'latest' for the most recent version,
    version="latest",
    # expand: which fields to materialize (markdown_full, text_full, items, *_content_metadata, ...),
    expand=["markdown"],
)

data = result.model_dump()
json_str = result.model_dump_json(indent=2)
print(json_str)