from pydantic import BaseModel


class GenesisRuntimeContext(BaseModel):
    pinecone_environment: str
    pinecone_api_key: str
    openai_api_key: str
    model_name: str
    model_tokens: int
    model_chunk_overlap: int
    model_dimension: int
    model_metric: str
    gpt_model_name: str
    client_id: str
