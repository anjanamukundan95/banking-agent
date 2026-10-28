from banking_agent.auth.authorization import authorize_account_access
from banking_agent.clients.banking_client import BankingClient

banking_client = BankingClient()

async def get_account_balance(
        user_id: str,
        account_id: str,
    ) -> dict:
        authorize_account_access(user_id, account_id)

        return await banking_client.get_balance(account_id)

async def get_recent_transactions(
        user_id: str,
        account_id: str,
        limit: int = 10,
    ) -> dict:
        authorize_account_access(user_id, account_id)
        limit = min(limit, 50)
        transactions = await banking_client.get_transactions(account_id, limit)
        return transactions
