from fastapi import Depends, FastAPI

from banking_agent.auth.auth_jwt import get_current_user
from banking_agent.models.rag import ChatRequest, ChatResponse
from banking_agent.services.agent_runner import run_banking_agent

app = FastAPI(title="Banking Agent", description="Banking Agent API", version="1.0.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    return await run_banking_agent(request.message, current_user)
