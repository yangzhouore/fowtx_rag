# ARCHITECTURE.md

## V0 Architecture

```text
User
 ↓
Next.js Web UI
 ↓
FastAPI
 ↓
RAG Service
 ├─ Retrieval
 ├─ OpenAI
 └─ Source formatting
 ↓
Chroma Vector Store
```

Document ingestion is separate from user queries:

```text
FOWT Documents
 ↓
Loader
 ↓
Text Splitter
 ↓
Embeddings
 ↓
Chroma
```

## Component Responsibilities

### `app/`

Owns the RAG domain logic:

- document loading
- chunking
- embeddings
- vector storage
- retrieval
- answer generation
- source handling

It should not contain frontend code.

### `api/`

Owns the HTTP interface.

Initial API surface:

```text
POST /query
GET  /health
```

The API should call the RAG layer rather than duplicate RAG logic.

### `web/`

Owns the user interface.

Initial UI should provide:

- question input
- answer display
- source citations
- loading/error states

Use Next.js, TypeScript, Tailwind CSS, shadcn/ui, and Lucide icons.

### `tests/`

Contains automated tests for core behaviour and API integration.

### `.github/workflows/`

Runs automated validation for pull requests and main-branch changes.

## Architectural Rules

- Keep the RAG core independent of the web UI.
- Keep HTTP handling out of the RAG domain layer.
- Preserve source metadata through retrieval and answer generation.
- Keep configuration in environment variables or configuration modules.
- Never expose OpenAI keys to the browser.
- Prefer the simplest implementation that satisfies V0 requirements.
- Chroma is acceptable for V0; database migration is a later decision.

## Out of Scope for V0

- authentication
- user accounts
- admin dashboard
- automated web crawling
- multi-agent runtime
- advanced reranking
- production-scale observability
- complex cloud infrastructure
