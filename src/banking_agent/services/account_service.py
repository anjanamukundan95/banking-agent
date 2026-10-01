from banking_agent.clients.banking_client import BankingClient

banking_client = BankingClient()


async def get_account_balance(account_id: str):
    """Fetch the balance for a given account ID."""
    return await banking_client.get_balance(account_id)


async def get_recent_transactions(
    account_id: str,
    limit: int = 10,
):
    """Fetch recent transactions for a given account ID."""
    return await banking_client.get_transactions(account_id, limit)