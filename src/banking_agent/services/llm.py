    # Get the OpenAI client for Responses API
from banking_agent.client import openai_client
from banking_agent.config import settings


def ask_model(question: str) -> str:
    response = openai_client.responses.create(
        model=settings.model_name,
        input=question,
    )

    return response.output_text