import httpx

from banking_agent.config import settings


class BankingClient:
    async def get_balance(self, account_id: str):
        url = f"{settings.banking_api_base_url}/api/v1/accounts/{account_id}/balance"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            return response.json()

    async def get_transactions(
        self,
        account_id: str,
        limit: int = 10,
    ):
        url = (
            f"{settings.banking_api_base_url}/api/v1/accounts/{account_id}/transactions"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={"limit": limit},
            )
            response.raise_for_status()
            return response.json()
