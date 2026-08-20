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
 ↓
Load
 ↓
Split
 ↓
Embed
 ↓
Chroma
 ↓
Retrieve
 ↓
LLM
 ↓
Answer + Sources
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

## Direction

Keep V0 small. Do not add user accounts, admin systems, crawlers, advanced evaluation pipelines, or complex infrastructure until the core online RAG works reliably.
