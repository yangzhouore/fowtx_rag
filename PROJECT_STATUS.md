# PROJECT_STATUS.md

## Current Stage

**Stage: Local RAG prototype -> Online V0**

The repository currently demonstrates the core RAG flow locally.

## Working Today

- PDF document loading
- text splitting
- OpenAI embeddings
- Chroma vector storage
- similarity retrieval
- LLM answer generation
- basic source/page reporting
- MVP-0 pytest and CI baseline
- FastAPI application skeleton
- `GET /health` endpoint
- `POST /query` endpoint

## V0 Target

Turn the existing local prototype into a small public web application.

## Next Tasks

- [x] Add FastAPI application
- [x] Add `POST /query`
- [x] Add `GET /health`
- [ ] Add Next.js frontend
- [ ] Add polished search/answer UI
- [ ] Connect frontend to API
- [ ] Show citations in the UI
- [x] Add basic backend tests
- [x] Add GitHub Actions CI
- [ ] Deploy frontend and backend

## Not Yet Needed

- advanced retrieval changes
- pgvector migration
- user authentication
- admin tools
- automated data crawling
- large evaluation framework
- complex agent orchestration

## Project Rule

Keep the next implementation step focused on getting the existing RAG online before expanding functionality.

Update this file whenever a major task is completed or the V0 scope changes.
