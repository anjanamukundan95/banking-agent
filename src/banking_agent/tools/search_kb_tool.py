from azure.ai.projects.models import FunctionTool

search_knowledge_tool = FunctionTool(
    name="search_knowledge",
    description="""
    Search the banking knowledge base for relevant policies,
    fees, account requirements, card information, KYC procedures,
    transactions, and complaint handling procedures.

    Use this tool when answering questions that require information
    from the banking knowledge base.
    """,
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query for finding relevant information in the banking knowledge base.",
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    },
    strict=True,
)
