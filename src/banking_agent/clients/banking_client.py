import logging

import httpx

from banking_agent.config import settings

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(10.0, connect=5.0)


class BankingClient:
    async def get_balance(self, account_id: str):
        url = f"{settings.banking_api_base_url}/api/v1/accounts/{account_id}/balance"
        logger.debug("Fetching balance for account %s", account_id)

        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
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
        logger.debug("Fetching %d transactions for account %s", limit, account_id)

        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            response = await client.get(
                url,
                params={"limit": limit},
            )
            response.raise_for_status()
            return response.json()
