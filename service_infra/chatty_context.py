from dataclasses import dataclass
from typing import Optional


@dataclass
class ChattyRuntimeContext:
    pinecone_environment: Optional[str] = None
    pinecone_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    model_name: Optional[str] = None
    model_tokens: Optional[int] = None
    model_chunk_overlap: Optional[int] = None
    model_dimension: Optional[int] = None
    model_metric: Optional[str] = None
    gpt_model_name: Optional[str] = None
    client_id: Optional[str] = None
