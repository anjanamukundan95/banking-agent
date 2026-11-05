# Banking Agent

UAE banking operations assistant built with Azure AI Foundry Agent Service, Azure AI Search (RAG), and FastAPI. Portfolio project targeting the **Azure AI-103** (Azure AI Apps and Agents Developer) certification.

---

## Architecture

```
Client
  └── POST /api/v1/chat  (JWT-authenticated)
        └── FastAPI (main.py)
              └── run_banking_agent (agent_runner.py)
                    ├── Content Safety check (input)
                    ├── Language Detection → response language instruction
                    ├── Azure AI Foundry — openai_client.responses.create()
                    │     ├── Tool: search_knowledge  → Azure AI Search (RAG)
                    │     ├── Tool: get_account_balance → Banking API (via httpx)
                    │     └── Tool: get_recent_transactions → Banking API (via httpx)
                    └── Content Safety check (output)

All requests traced → Application Insights
```

---

## AI-103 Coverage

| Domain | Weight | Features Implemented |
|---|---|---|
| D1 — Plan & Manage | 25–30% | Application Insights telemetry, RBAC across all services, structured logging |
| D2 — Generative AI & Agents | 30–35% | Azure AI Foundry agent, RAG with citations, function calling, Content Safety |
| D4 — Text Analysis | 10–15% | Language detection (Arabic/English routing) |
| D5 — Information Extraction | 10–15% | Coming soon: Document Intelligence |

---

## Project Structure

```
src/banking_agent/
├── auth/
│   ├── auth_jwt.py              # JWT validation via Microsoft Entra ID (PyJWKClient)
│   └── authorization.py         # Account access control per user (temp in-memory store)
├── clients/
│   └── banking_client.py        # Async HTTP client for banking API (httpx, 10s timeout)
├── models/
│   └── rag.py                   # Pydantic models: ChatRequest, ChatResponse, Citation, KnowledgeChunk
├── services/
│   ├── agent.py                 # create_banking_agent() — registers tools with Foundry
│   ├── agent_runner.py          # run_banking_agent() — orchestrates tool calls and citations
│   ├── account_service.py       # Business logic: balance + transactions with authz checks
│   ├── content_safety.py        # Input/output safety checks via Azure AI Content Safety
│   ├── language_detection.py    # Language detection (Arabic/English) via Azure AI Language
│   ├── rag.py                   # search_knowledge() — Azure AI Search vector+semantic hybrid
│   ├── tool_executor.py         # Dispatches tool calls from agent to service functions
│   └── llm.py                   # ask_model() — direct model call (used in tests)
├── tools/
│   ├── banking_tools.py         # FunctionTool definitions for balance + transactions
│   └── search_kb_tool.py        # FunctionTool definition for knowledge base search
├── evaluation/
│   ├── retrieval.py             # Metrics: recall@k, precision@k, NDCG@k, MRR
│   ├── run_retrieval_eval.py    # Runs retrieval evaluation against test dataset
│   └── dataset/
│       └── retrieval_dataset.py # 5 labelled test queries with relevant sources
├── client.py                    # AIProjectClient + openai_client initialisation
├── config.py                    # Settings via pydantic-settings (reads .env)
├── create_agent.py              # One-time script to register agent in Foundry
└── main.py                      # FastAPI app — /health + /api/v1/chat + App Insights

tests/
├── test_agent.py                # Integration test for full agent response
├── test_banking_client.py       # Async tests for BankingClient (requires WireMock)
├── test_rag.py                  # Integration test for Azure AI Search retrieval
└── az_conn_test.py              # Manual smoke test for Azure client + LLM connection
```

---

## Azure Services Used

| Service | Purpose | Auth |
|---|---|---|
| Azure AI Foundry (azure-ai-projects) | Agent hosting, tool registration, conversation management | DefaultAzureCredential |
| Azure OpenAI | Language model via Foundry Responses API | DefaultAzureCredential |
| Azure AI Search | Vector + semantic hybrid RAG over banking policy documents | DefaultAzureCredential + RBAC |
| Azure AI Content Safety | Input/output harmful content detection | DefaultAzureCredential + RBAC |
| Azure AI Language | Language detection for Arabic/English routing | DefaultAzureCredential + RBAC |
| Azure Monitor / Application Insights | Request tracing, dependency tracking, logging | Connection string |
| Azure Identity (DefaultAzureCredential) | Passwordless auth chain across all services | — |
| Microsoft Entra ID | JWT-based user authentication on the `/chat` endpoint | — |

---

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Azure CLI (`az`)
- An Azure subscription with:
  - Azure AI Foundry project
  - Azure AI Search service
  - Azure AI Content Safety resource
  - Azure AI Language resource
  - Application Insights resource

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-foundry-resource>.services.ai.azure.com/api/projects/<project>
MODEL_NAME=gpt-4o

AZURE_SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AZURE_SEARCH_INDEX_NAME=<your-index-name>
AZURE_SEARCH_SEMANTIC_CONFIGURATION=<your-semantic-config-name>

CONTENT_SAFETY_ENDPOINT=https://<your-content-safety>.cognitiveservices.azure.com/

LANGUAGE_ENDPOINT=https://<your-language-resource>.cognitiveservices.azure.com/

APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...

AZURE_AI_AGENT_NAME=uae-banking-agent
BANKING_API_BASE_URL=http://localhost:8090

AUTH_ISSUER=https://sts.windows.net/<tenant-id>/
AUTH_AUDIENCE=api://<app-registration-client-id>
AUTH_JWKS_URL=https://login.microsoftonline.com/<tenant-id>/discovery/v2.0/keys
```

### 3. Azure RBAC — assign required roles

Your identity (or managed identity in production) needs these roles:

| Role | Resource |
|---|---|
| `Azure AI Developer` | Azure AI Foundry project |
| `Search Index Data Reader` | Azure AI Search service |
| `Cognitive Services User` | Azure AI Content Safety resource |
| `Cognitive Services Language Reader` | Azure AI Language resource |

```bash
# Get your object ID
az ad signed-in-user show --query id -o tsv

# Assign each role (repeat for each resource)
az role assignment create \
  --role "<role-name>" \
  --assignee <your-object-id> \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/<resource-provider>/<resource-name>
```

### 4. Enable RBAC on Cognitive Services resources

By default Azure Cognitive Services only allow API key auth. For each of these resources — **AI Search**, **Content Safety**, **Language** — enable RBAC via the portal:

1. Go to the resource → **Keys and Endpoint** → **API access control**
2. Select **"Both (API keys and role-based access control)"**
3. Click **Save**

> Without this step, `DefaultAzureCredential` will receive 403/PermissionDenied even with the correct role assigned.

### 5. Login with Azure CLI

```bash
az login --tenant <your-tenant-id>
```

### 6. Create the agent in Foundry

```bash
uv run python -m banking_agent.create_agent
```

### 7. Start the mock banking API (for local dev)

```bash
cd wire-mock && docker compose up -d
```

### 8. Run the app

```bash
uv run uvicorn banking_agent.main:app --reload
```

API available at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

---

## Running Tests

```bash
# All tests (requires WireMock running and Azure connectivity)
uv run pytest

# RAG retrieval test only
uv run pytest tests/test_rag.py -v

# Banking client test only (requires WireMock)
uv run pytest tests/test_banking_client.py -v
```

---

## Retrieval Evaluation

```bash
uv run python -m banking_agent.evaluation.run_retrieval_eval
```

Outputs Recall@3, NDCG@3, MRR, and Precision@3 over the 5-query test dataset.

---

## Guardrails — Content Safety

Every message is checked before reaching the agent and every response is checked before being returned.

| Layer | What it catches |
|---|---|
| Input severity check | Explicit hate, violence, sexual, self-harm content (severity ≥ 2) |
| Output severity check | Agent responses that contain harmful content |
| Foundry model filters | Ambiguous harmful intent the severity check won't catch |

Input violations return HTTP `400`. Output violations return a safe fallback message.

---

## Language Detection

Every incoming message is analysed by Azure AI Language service. The detected language (Arabic or English) is appended as an explicit instruction to the agent, ensuring consistent bilingual responses. Unsupported languages fall back to English.

---

## Observability — Application Insights

All requests are automatically traced end-to-end. In Application Insights you can see:

| View | What it shows |
|---|---|
| **Transaction search → Requests** | Every `/api/v1/chat` call with latency and status |
| **Dependencies** | Calls to Azure Search, OpenAI, Content Safety, Language with per-call latency |
| **Failures** | Exceptions with full stack traces |
| **Logs (KQL)** | All `logger.warning/debug` calls from services |

Sample KQL query:
```kusto
requests
| where timestamp > ago(30m)
| project timestamp, name, duration, resultCode
| order by timestamp desc
```

---

## API

### `POST /api/v1/chat`

Requires `Authorization: Bearer <JWT>` header.

**Request:**
```json
{ "message": "What are the fees for international card transactions?" }
```

**Response:**
```json
{
  "answer": "International card transactions incur a 2.5% foreign currency fee **[1]**.",
  "citations": [
    { "citation_id": "[1]", "title": "Card Fees and Charges Policy" }
  ]
}
```

**Arabic example:**
```json
{ "message": "ما هو رصيد حسابي؟" }
```

### `GET /health`

```json
{ "status": "ok" }
```

---

## Known Limitations

- `authorization.py` — user-to-account mapping is hardcoded (replace with database/entitlement service for production)
- Sessions are stateless per-request (conversation history managed by Foundry via `conversation.id`)
- Document Intelligence (D5) not yet implemented
- Azure AI Evaluation SDK integration pending
