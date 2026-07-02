from gliner2 import GLiNER2
from app.utils.helper import get_gliner2_structure_format


class MetaDataExtractor:
    def __init__(self, model: GLiNER2, threshold: float = 0.6):
        self.model = model
        self.threshold = threshold
        self.metadata_model = get_gliner2_structure_format()
    
    @classmethod
    def from_pretrained(cls,model_name: str = "fastino/gliner2-base-v1", threshold: float = 0.6) -> "MetaDataExtractor":
        model = GLiNER2.from_pretrained(model_name)
        return cls(model=model, threshold=threshold)
    
    def _extract_response(self, extraction_result):
        if not isinstance(extraction_result, dict):
            return extraction_result

        if isinstance(extraction_result.get("entities"), dict):
            extraction_result = extraction_result["entities"]

        return extraction_result.get("response", extraction_result)


    def extract(self, pages: list[dict]) -> list[dict]:
        chunks_with_metadata = []
        for page in pages:
            text = page["markdown"]
            if not text:
                continue
            try:
                extraction_result = self.model.extract_json(
                    text,
                    self.metadata_model,
                    threshold=self.threshold,
                )
            except TypeError:
                extraction_result = self.model.extract_json(text, self.metadata_model)

            page_metadata = {k: v for k, v in page.items() if k != "markdown"}
            response = self._extract_response(extraction_result)
            if isinstance(response, dict):
                page_metadata.update(response)
            else:
                page_metadata["response"] = response

            chunks_with_metadata.append(
                {
                    "chunk": text,
                    "metadata": page_metadata,
                }
            )

        return chunks_with_metadata
