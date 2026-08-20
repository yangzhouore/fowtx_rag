# AGENTS.md

## Mission

Build and maintain **FOWTX RAG** as a simple online knowledge base for floating offshore wind (FOWT).

The current priority is the smallest useful online product:

**Ask → Retrieve → Answer → Cite sources**

## Working Rules

- Read `README.md`, `ARCHITECTURE.md`, and `PROJECT_STATUS.md` before making changes.
- Prefer small, focused changes over large refactors.
- Preserve working RAG behaviour unless the task explicitly requires a change.
- Keep backend, API, and frontend responsibilities separated.
- Do not add dependencies unless they are necessary.
- Never commit API keys, secrets, local databases, or generated data.
- Keep source citations visible in RAG answers.
- Update documentation when architecture or project status changes.

## Expected Structure

- `app/` — RAG and ingestion logic
- `api/` — FastAPI service
- `web/` — Next.js frontend
- `tests/` — automated tests
- `.github/workflows/` — CI/CD workflows

## Definition of Done

Before completing a task:

1. Run relevant tests or checks.
2. Run Python linting for backend changes.
3. Run frontend lint/build for frontend changes.
4. Confirm no secrets or generated data were added.
5. Update `PROJECT_STATUS.md` if project capability changed.
6. Summarize what changed and any remaining limitations.

## Change Discipline

Do not redesign the whole project for a local task.

If a requested change conflicts with `ARCHITECTURE.md`, call out the conflict before changing the architecture.
