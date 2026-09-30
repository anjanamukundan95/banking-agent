
from banking_agent.services.agent_runner import run_banking_agent


def test_banking_agent():
    question = "What fees can apply to international card transactions?"

    answer = run_banking_agent(question)

    print("\nAGENT RESPONSE:")
    print(answer)

    assert answer