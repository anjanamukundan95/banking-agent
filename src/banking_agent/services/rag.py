from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery

from banking_agent.config import settings
from banking_agent.models.rag import (
    KnowledgeChunk,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
)

search_client = SearchClient(
    endpoint=settings.azure_search_endpoint,
    index_name=settings.azure_search_index_name,
    credential=DefaultAzureCredential(),
)


def search_knowledge(
    request: KnowledgeSearchRequest,
) -> KnowledgeSearchResponse:
    """
    Search the banking knowledge base for relevant policies,
    fees, account requirements, card information, KYC procedures,
    transactions, and complaint handling procedures.

    Use this tool when answering questions that require information
    from the banking knowledge base.
    """
    vector_query = VectorizableTextQuery(
        text=request.query,
        k_nearest_neighbors=request.top_k,
        fields="text_vector",
    )

    results = search_client.search(
        search_text=request.query,
        vector_queries=[vector_query],
        query_type="semantic",
        semantic_configuration_name=(settings.azure_search_semantic_configuration),
        select=[
            "chunk_id",
            "parent_id",
            "title",
            "chunk",
        ],
        top=request.top_k,
    )

    chunks: list[KnowledgeChunk] = []

    for index, result in enumerate(results, start=1):
        chunks.append(
            KnowledgeChunk(
                citation_id=f"[{index}]",
                chunk_id=result["chunk_id"],
                parent_id=result["parent_id"],
                title=result["title"],
                content=result["chunk"],
                score=result["@search.score"],
            )
        )

    return KnowledgeSearchResponse(
        query=request.query,
        results=chunks,
    )
