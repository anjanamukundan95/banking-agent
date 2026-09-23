from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from banking_agent.config import settings

#Create client to Connect to Microsoft Foundry project
project_client = AIProjectClient(
    endpoint=settings.azure_ai_project_endpoint, credential=DefaultAzureCredential()
)

# Get the OpenAI client for Responses API
openai_client = project_client.get_openai_client()
