from pydantic import BaseModel, Field


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Natural-language banking knowledge query",
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of knowledge chunks to retrieve",
    )


class KnowledgeChunk(BaseModel):
    citation_id: str
    chunk_id: str
    parent_id: str
    title: str
    content: str
    score: float


class KnowledgeSearchResponse(BaseModel):
    query: str
    results: list[KnowledgeChunk]

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )


class ChatResponse(BaseModel):
    answer: str
    citations: list["Citation"] = Field(default_factory=list)

class Citation(BaseModel):
    citation_id: str
    title: str