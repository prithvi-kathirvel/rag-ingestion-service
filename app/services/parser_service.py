from llama_cloud import LlamaCloud
from app.core.logging import logger
from app.services.metadata_service import MetaDataExtractor


class ParserService:
    def __init__(self, api_key: str, metadata_extractor: MetaDataExtractor):
        self.client = LlamaCloud(api_key=api_key)
        self.metadata_extractor = metadata_extractor

    async def parse_file(self, file_content: bytes, filename: str) -> list[dict]:
        logger.info(f"Parsing file: {filename}")
        try:
            uploaded_file = self.client.files.create(file=file_content, purpose="parse")
            result = self.client.parsing.parse(
                file_id=uploaded_file.id,
                tier="agentic",
                version="latest",
                expand=["markdown"]
            )
            pages = [page.model_dump() for page in result.markdown.pages]
            chunks_with_metadata = self.metadata_extractor.extract(pages)
            return chunks_with_metadata

        except Exception as e:
            logger.error(f"Error parsing file {filename}: {str(e)}")
            raise
