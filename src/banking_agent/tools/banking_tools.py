from azure.ai.projects.models import FunctionTool

get_account_balance_tool = FunctionTool(
    name="get_account_balance",
    description="Fetch the balance for a given account ID.",
    parameters={
        "type": "object",
        "properties": {
            "account_id": {
                "type": "string",
                "description": "The ID of the account for which to fetch the balance.",
            }
        },
        "required": ["account_id"],
        "additionalProperties": False,
    },
    strict=True,
)
get_recent_transactions_tool = FunctionTool(
    name="get_recent_transactions",
    description="Fetch recent transactions for a bank account.",
    parameters={
        "type": "object",
        "properties": {
            "account_id": {
                "type": "string",
                "description": "The bank account ID.",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of transactions to return.",
            },
        },
        "required": ["account_id", "limit"],
        "additionalProperties": False,
    },
    strict=True,
)
