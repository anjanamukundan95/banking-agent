from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi import Depends, FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from banking_agent.auth.auth_jwt import get_current_user
from banking_agent.config import settings
from banking_agent.models.rag import ChatRequest, ChatResponse
from banking_agent.services.agent_runner import run_banking_agent

configure_azure_monitor(
    connection_string=settings.application_insights_connection_string
)

app = FastAPI(title="Banking Agent", description="Banking Agent API", version="1.0.0")

FastAPIInstrumentor.instrument_app(app)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    return await run_banking_agent(request.message, current_user)
