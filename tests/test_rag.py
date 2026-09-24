from banking_agent.models.rag import KnowledgeSearchRequest
from banking_agent.services.rag import search_knowledge


def test_rag_search():
    request = KnowledgeSearchRequest(
        query="What fees can apply to international card transactions?",
        top_k=5,
    )

    response = search_knowledge(request)

    assert response.query == request.query
    assert response.results
    assert len(response.results) <= request.top_k

    citation_ids = {result.citation_id for result in response.results}

    assert citation_ids == {
        f"[{index}]" for index in range(1, len(response.results) + 1)
    }

    for result in response.results:
        assert result.chunk_id
        assert result.title
        assert result.content
        assert result.score is not None

        print(f"\n{result.citation_id} {result.title}")
        print(f"Score: {result.score}")
        print(f"Content: {result.content[:300]}...")
