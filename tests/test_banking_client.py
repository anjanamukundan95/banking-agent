import pytest

from banking_agent.clients.banking_client import BankingClient


@pytest.mark.asyncio
async def test_get_balance():
    client = BankingClient()

    result = await client.get_balance("ACC-10001")

    assert result["accountId"] == "ACC-10001"
    assert result["currency"] == "AED"
    assert result["availableBalance"] == 12450.75
    assert result["currentBalance"] == 13200.75


@pytest.mark.asyncio
async def test_get_transactions():
    client = BankingClient()

    result = await client.get_transactions("ACC-10001")

    assert result[0]["transactionId"] == "TXN-10001"
