import pytest

from banking_agent.services.agent_runner import run_banking_agent

_MOCK_USER = {"oid": "6065a318-4a9c-4467-992c-c82b760322e3"}


@pytest.mark.asyncio
async def test_banking_agent():
    question = "What fees can apply to international card transactions?"

    answer = await run_banking_agent(question, current_user=_MOCK_USER)

    print("\nAGENT RESPONSE:")
    print(answer)

    assert answer