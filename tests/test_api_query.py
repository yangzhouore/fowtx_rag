from fastapi.testclient import TestClient
from langchain_core.documents import Document

from api.main import app
from app import query as query_module
from app.query import answer_question, format_docs


def test_query_endpoint_returns_answer_and_sources(monkeypatch):
    def fake_answer_question(question):
        assert question == "What is a semi-submersible?"
        return {
            "answer": "A semi-submersible is a floating platform.",
            "sources": ["source.pdf (page 1)"],
        }

    monkeypatch.setattr("api.main.answer_question", fake_answer_question)
    client = TestClient(app)

    response = client.post(
        "/query",
        json={"question": "What is a semi-submersible?"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "A semi-submersible is a floating platform.",
        "sources": ["source.pdf (page 1)"],
    }


def test_query_endpoint_rejects_empty_question(monkeypatch):
    called = False

    def fake_answer_question(question):
        nonlocal called
        called = True
        return {"answer": "unused", "sources": []}

    monkeypatch.setattr("api.main.answer_question", fake_answer_question)
    client = TestClient(app)

    response = client.post("/query", json={"question": ""})

    assert response.status_code == 400
    assert called is False


def test_query_endpoint_rejects_whitespace_question(monkeypatch):
    called = False

    def fake_answer_question(question):
        nonlocal called
        called = True
        return {"answer": "unused", "sources": []}

    monkeypatch.setattr("api.main.answer_question", fake_answer_question)
    client = TestClient(app)

    response = client.post("/query", json={"question": "   "})

    assert response.status_code == 400
    assert called is False


def test_query_endpoint_returns_503_for_rag_runtime_failure(monkeypatch):
    def fake_answer_question(question):
        raise RuntimeError("vector store unavailable")

    monkeypatch.setattr("api.main.answer_question", fake_answer_question)
    client = TestClient(app)

    response = client.post("/query", json={"question": "What is FOWT?"})

    assert response.status_code == 503
    assert response.json() == {"detail": "RAG service unavailable"}


def test_answer_question_retrieves_once_and_uses_retrieved_docs(monkeypatch):
    docs = [
        Document(page_content="First context", metadata={"source": "a.pdf", "page": 0}),
        Document(page_content="Second context", metadata={"source": "b.pdf", "page": 1}),
        Document(page_content="Repeated source", metadata={"source": "a.pdf", "page": 0}),
    ]
    calls = {"retrieve": 0, "llm_inputs": []}

    class FakeRetriever:
        def invoke(self, question):
            calls["retrieve"] += 1
            assert question == "What is floating wind?"
            return docs

    class FakeVectorStore:
        def as_retriever(self, search_kwargs):
            assert search_kwargs == {"k": query_module.RETRIEVAL_K}
            return FakeRetriever()

    class FakeLLM:
        def __init__(self, model, temperature):
            assert model == query_module.LLM_MODEL
            assert temperature == 0

    class FakePrompt:
        def __or__(self, other):
            assert isinstance(other, FakeLLM)
            return FakePipeline()

    class FakePipeline:
        def __or__(self, other):
            assert isinstance(other, FakeParser)
            return FakeChain()

    class FakeParser:
        pass

    class FakeChain:
        def invoke(self, payload):
            calls["llm_inputs"].append(payload)
            return "Answer from retrieved context"

    monkeypatch.setattr(query_module, "load_vectorstore", lambda: FakeVectorStore())
    monkeypatch.setattr(query_module, "ChatOpenAI", FakeLLM)
    monkeypatch.setattr(query_module, "StrOutputParser", FakeParser)
    monkeypatch.setattr(query_module, "prompt", FakePrompt())

    result = answer_question("What is floating wind?")

    assert calls["retrieve"] == 1
    assert calls["llm_inputs"] == [
        {
            "context": format_docs(docs),
            "question": "What is floating wind?",
        }
    ]
    assert result == {
        "answer": "Answer from retrieved context",
        "sources": ["a.pdf (page 1)", "b.pdf (page 2)"],
    }