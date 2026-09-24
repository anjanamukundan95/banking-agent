import pytest

from banking_agent.evaluation.dataset.retrieval_dataset import RETRIEVAL_TEST_CASES
from banking_agent.models.rag import KnowledgeSearchRequest
from banking_agent.services.rag import search_knowledge


@pytest.mark.parametrize(
    "test_case",
    RETRIEVAL_TEST_CASES,
)
def test_retrieval_relevance(test_case):
    request = KnowledgeSearchRequest(
        query=test_case.query,
        top_k=5,
    )

    response = search_knowledge(request)

    retrieved_sources = {result.title for result in response.results}

    assert retrieved_sources.intersection(test_case.relevant_sources), (
        f"No relevant source retrieved for query: "
        f"{test_case.query}\n"
        f"Relevant: {test_case.relevant_sources}\n"
        f"Retrieved: {retrieved_sources}"
    )
