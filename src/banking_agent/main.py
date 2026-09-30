from fastapi import FastAPI

from banking_agent.models.rag import ChatRequest, ChatResponse
from banking_agent.services.agent_runner import run_banking_agent

app = FastAPI(title="Banking Agent", description="Banking Agent API", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return run_banking_agent(request.message)
