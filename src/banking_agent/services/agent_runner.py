import json
import logging
import re

logger = logging.getLogger(__name__)

from fastapi import HTTPException
from openai.types.responses.response_input_param import ResponseInputParam

from banking_agent.client import project_client
from banking_agent.config import settings
from banking_agent.models.rag import (
    ChatResponse,
    Citation,
)
from banking_agent.services.content_safety import check_text
from banking_agent.services.language_detection import detect_language
from banking_agent.services.tool_executor import execute_tool

_CITATION_PATTERN = re.compile(r"\*\*\[(\d+)\]\*\*")


async def run_banking_agent(question: str, current_user: dict) -> ChatResponse:
    input_check = check_text(question)
    if input_check["blocked"]:
        raise HTTPException(
            status_code=400,
            detail=f"Message blocked by Content Safety: {input_check['reason']}",
        )
    user_id = current_user.get("oid")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Token does not contain a valid user identity",
        )
    # detect language and instruct agent explicitly                                                                                                                                
    lang = detect_language(question)                                                                                                                                               
    lang_label = "Arabic" if lang == "ar" else "English"                                                                                                                           
    augmented_question = f"{question}\n\n[System: Please respond in {lang_label}]"                                                                                                                                                               
    openai_client = project_client.get_openai_client()

    conversation = openai_client.conversations.create()

    response = openai_client.responses.create(
        conversation=conversation.id,
        input=augmented_question,
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

        arguments = json.loads(item.arguments)

        result = await execute_tool(
            item.name,
            arguments,
            user_id=user_id,
        )

        if item.name == "search_knowledge":
            retrieved_chunks.extend(result.results)

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(
                    result.model_dump() if hasattr(result, "model_dump") else result
                ),
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
    output_check = check_text(answer)
    if output_check["blocked"]:
        logger.warning("Agent output blocked by Content Safety")
        answer = "I'm unable to provide a response to that request."

    citations = _validate_and_build_citations(answer, retrieved_chunks)
    return ChatResponse(answer=answer, citations=citations)


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
            logger.warning(
                "Agent returned citation %s but it was not in retrieved chunks — skipping",
                citation_id,
            )
            continue

        citations.append(
            Citation(
                citation_id=chunk.citation_id,
                title=chunk.title,
            )
        )

    return citations
