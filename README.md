# FOWTX RAG

A lightweight online RAG knowledge base for **floating offshore wind (FOWT)**.

## Goal

Provide a simple interface where users can ask FOWT engineering or research questions and receive grounded answers with source citations.

## V0 Scope

The first online version only needs to support:

- ingest FOWT documents
- create embeddings
- retrieve relevant document chunks
- generate grounded answers
- return source citations
- expose the RAG through a small API
- provide a clean web interface

## Planned Stack

- **Backend:** Python
- **RAG:** OpenAI + LangChain
- **Vector store:** Chroma initially
- **API:** FastAPI
- **Frontend:** Next.js + TypeScript
- **UI:** Tailwind CSS + shadcn/ui
- **CI/CD:** GitHub Actions
- **Development control:** Codex + repository harness files

## Current RAG Flow

```text
PDF
 -> Load
 -> Split
 -> Embed
 -> Chroma
 -> Retrieve
 -> LLM
 -> Answer + Sources
```

## Repository Guidance

Before making changes, read:

- `AGENTS.md`
- `ARCHITECTURE.md`
- `PROJECT_STATUS.md`

## Local Setup

Create and activate a Python virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Add required environment variables using `.env.example`.

## Validation

Run the backend checks from the repository root:

```bash
python -m compileall app api tests
ruff check app api tests
pytest -q
```

Run the frontend checks from `web/`:

```bash
npm ci
npm run lint
npm run test
npm run build
```

The frontend build uses `next/font/google`, so the build environment must be able to reach Google Fonts or the fonts should be changed to a local font setup before deployment.

## Deployment Preparation

V0 uses two deployable services:

- **Backend:** FastAPI service exposing `GET /health`, `GET /ready`, and `POST /query`
- **Frontend:** Next.js app in `web/`, with a server-side `/api/query` route that forwards requests to FastAPI

The browser should call the Next.js app, not the FastAPI service directly. This keeps API routing server-side and avoids exposing OpenAI credentials to the browser.

### Backend Deployment

Deploy the backend to a Python web host such as Render, Railway, Fly.io, or a small VM.

Expected backend runtime command:

```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

If the chosen host does not provide `uvicorn`, add it to the backend runtime dependencies before deploying.

Required backend environment variables:

```bash
OPENAI_API_KEY=...
```

Optional backend environment variables:

```bash
LANGCHAIN_API_KEY=...
```

`LANGCHAIN_API_KEY` is only needed if LangChain tracing or related hosted LangChain features are intentionally enabled.

### Frontend Deployment

Deploy `web/` to a Next.js-capable host such as Vercel, Render, Railway, or a Node server. The frontend must support Next.js route handlers; do not deploy it as a static-only site for V0.

Required frontend environment variables:

```bash
FOWTX_API_BASE_URL=https://your-backend-host.example
```

For local development, `web/.env.example` uses:

```bash
FOWTX_API_BASE_URL=http://127.0.0.1:8000
```

Frontend build command:

```bash
cd web
npm ci
npm run build
```

Frontend start command for a generic Node host:

```bash
npm run start
```

### Chroma Vector Store Expectations

The Chroma vector store is currently local at:

```text
data/chroma_db
```

Generated vector data and source documents must not be committed. The repository `.gitignore` excludes `data/` for this reason.

For production V0, use one of these approaches:

- Build `data/chroma_db` during deployment from production-provided source documents stored outside git.
- Attach persistent storage to the backend host and run ingestion once before serving traffic.
- Build the vector store locally, then upload it to the backend host as a private deployment artifact outside git.

The backend will return unavailable responses if `data/chroma_db` is missing, empty, incompatible with the configured collection, or inaccessible at runtime.

### CORS and API URL

No backend CORS middleware is required for the current V0 path because:

```text
Browser -> Next.js /api/query -> FastAPI /query
```

Add backend CORS only if a future frontend calls FastAPI directly from the browser.

### Smoke Tests

After deploying the backend, check health:

```bash
curl https://your-backend-host.example/health
```

Expected response:

```json
{"status":"ok"}
```

Check readiness:

```bash
curl https://your-backend-host.example/ready
```

Expected shape:

```json
{
  "status": "ready",
  "checks": {
    "openai_api_key": true,
    "vectorstore_path": true,
    "vectorstore_loadable": true
  }
}
```

Check the query endpoint:

```bash
curl -X POST https://your-backend-host.example/query \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is floating offshore wind?\"}"
```

Expected shape:

```json
{
  "answer": "...",
  "sources": ["source.pdf (page 1)"]
}
```

After deploying the frontend:

1. Open the deployed frontend URL.
2. Enter a FOWT question.
3. Confirm the loading state appears.
4. Confirm an answer appears.
5. Confirm source citations are visible.
6. Temporarily misconfigure `FOWTX_API_BASE_URL` in a non-production environment and confirm the error state is visible.

## Direction

Keep V0 small. Do not add user accounts, admin systems, crawlers, advanced evaluation pipelines, or complex infrastructure until the core online RAG works reliably.
