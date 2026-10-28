import logging

from banking_agent.models.rag import KnowledgeSearchRequest
from banking_agent.services import account_service
from banking_agent.services.rag import search_knowledge

logger = logging.getLogger(__name__)


def _search_knowledge(query: str):
    request = KnowledgeSearchRequest(
        query=query,
        top_k=3,
    )
    return search_knowledge(request)


async def execute_tool(
    tool_name: str,
    arguments: dict,
    user_id: str,
):
    logger.debug("Executing tool %s with args %s", tool_name, arguments)

    if tool_name == "get_account_balance":
        return await account_service.get_account_balance(user_id, **arguments)

    if tool_name == "get_recent_transactions":
        return await account_service.get_recent_transactions(user_id, **arguments)

    if tool_name == "search_knowledge":
        return _search_knowledge(**arguments)

    raise ValueError(f"Unknown tool: {tool_name}")