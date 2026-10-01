from banking_agent.models.rag import KnowledgeSearchRequest
from banking_agent.services.account_service import (
    get_account_balance,
    get_recent_transactions,
)
from banking_agent.services.rag import search_knowledge


async def _search_knowledge(query: str):
    request = KnowledgeSearchRequest(
        query=query,
        top_k=3,
    )

    return search_knowledge(request)


TOOL_HANDLERS = {
    "search_knowledge": _search_knowledge,
    "get_account_balance": get_account_balance,
    "get_recent_transactions": get_recent_transactions,
}


async def execute_tool(
    tool_name: str,
    arguments: dict,
):
    handler = TOOL_HANDLERS.get(tool_name)

    if handler is None:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    return await handler(**arguments)