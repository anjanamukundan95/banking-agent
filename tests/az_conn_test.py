from banking_agent.client import project_client
from banking_agent.services.llm import ask_model


def test_project_client_initialization():
    print("Testing project client initialization...")
    assert project_client is not None


def test_ask_model():
    question = "What is the capital of France?"
    response = ask_model(question)
    print(f"Response from model: {response}")
    assert response is not None
    assert isinstance(response, str)
    
test_project_client_initialization()
test_ask_model()
