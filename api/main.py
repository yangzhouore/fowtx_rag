import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.config import DB_DIR

app = FastAPI(title="FOWTX RAG API")


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


def answer_question(question: str):
    from app.query import answer_question as run_rag_query

    return run_rag_query(question)


def load_ready_vectorstore():
    from app.vectorstore import load_vectorstore

    return load_vectorstore()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    checks = {
        "openai_api_key": bool(os.getenv("OPENAI_API_KEY")),
        "vectorstore_path": DB_DIR.exists(),
        "vectorstore_loadable": False,
    }

    if checks["vectorstore_path"]:
        try:
            load_ready_vectorstore()
            checks["vectorstore_loadable"] = True
        # Readiness should report dependency failures instead of leaking internals.
        except Exception:  # noqa: BLE001
            checks["vectorstore_loadable"] = False

    if all(checks.values()):
        return {"status": "ready", "checks": checks}

    raise HTTPException(
        status_code=503,
        detail={"status": "unavailable", "checks": checks},
    )


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty")

    try:
        return answer_question(question)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="RAG service unavailable",
        ) from exc
