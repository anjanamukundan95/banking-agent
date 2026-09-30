import json
import re

from openai.types.responses.response_input_param import ResponseInputParam

from banking_agent.client import project_client
from banking_agent.config import settings
from banking_agent.models.rag import (
    ChatResponse,
    Citation,
    KnowledgeSearchRequest,
)
from banking_agent.services.rag import search_knowledge

_CITATION_PATTERN = re.compile(r"\[(\d+)\]")


def run_banking_agent(question: str) -> ChatResponse:
    openai_client = project_client.get_openai_client()

    conversation = openai_client.conversations.create()

    response = openai_client.responses.create(
        conversation=conversation.id,
        input=question,
        extra_body={
            "agent_reference": {
                "name": settings.azure_ai_agent_name,
                "type": "agent_reference",
            }
        },
    )

    tool_outputs: ResponseInputParam = []

    retrieved_chunks = []

    for item in response.output:
        if item.type != "function_call":
            continue

        if item.name != "search_knowledge":
            continue

        arguments = json.loads(item.arguments)

        request = KnowledgeSearchRequest(
            query=arguments["query"],
            top_k=3,
        )

        search_response = search_knowledge(request)

        retrieved_chunks.extend(search_response.results)

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(search_response.model_dump()),
            }
        )

    if not tool_outputs:
        return ChatResponse(
            answer=response.output_text,
            citations=[],
        )

    final_response = openai_client.responses.create(
        conversation=conversation.id,
        input=tool_outputs,
        extra_body={
            "agent_reference": {
                "name": settings.azure_ai_agent_name,
                "type": "agent_reference",
            }
        },
    )

    answer = final_response.output_text

    citations = _validate_and_build_citations(
        answer,
        retrieved_chunks,
    )

    return ChatResponse(
        answer=answer,
        citations=citations,
    )


def _validate_and_build_citations(
    answer: str,
    retrieved_chunks,
) -> list[Citation]:

    citation_numbers = {int(match) for match in _CITATION_PATTERN.findall(answer)}

    citations_by_id = {chunk.citation_id: chunk for chunk in retrieved_chunks}

    citations: list[Citation] = []

    for number in sorted(citation_numbers):
        citation_id = f"[{number}]"

        chunk = citations_by_id.get(citation_id)

        if chunk is None:
            raise ValueError(f"Invalid citation {citation_id} returned by agent")

        citations.append(Citation(citation_id=chunk.citation_id, title=chunk.title))

    return citations
