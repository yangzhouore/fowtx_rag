from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.query import answer_question

app = FastAPI(title="FOWTX RAG API")


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


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
