from banking_agent.models.rag import KnowledgeSearchRequest
from banking_agent.services import account_service
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
    return await search_knowledge(request)


TOOL_HANDLERS = {
    "search_knowledge": _search_knowledge,
    "get_account_balance": get_account_balance,
    "get_recent_transactions": get_recent_transactions,
}

USER_SCOPED_TOOLS = {
    "get_account_balance",
    "get_recent_transactions",
}


async def execute_tool(
    tool_name: str,
    arguments: dict,
    user_id: str,
):

    if tool_name == "get_account_balance":
        return await account_service.get_account_balance(user_id,
            **arguments
        )

    if tool_name == "get_recent_transactions":
        return await account_service.get_recent_transactions(
            user_id,
            **arguments
        )

    if tool_name == "search_knowledge":
        return await _search_knowledge(
            **arguments
        )

    raise ValueError(
        f"Unknown tool: {tool_name}"
    )