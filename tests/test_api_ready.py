from pathlib import Path

from fastapi.testclient import TestClient

from api import main as api_main


def test_ready_endpoint_returns_ready_when_dependencies_are_available(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(api_main, "DB_DIR", Path("."))
    monkeypatch.setattr(api_main, "load_ready_vectorstore", lambda: object())

    client = TestClient(api_main.app)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {
            "openai_api_key": True,
            "vectorstore_path": True,
            "vectorstore_loadable": True,
        },
    }


def test_ready_endpoint_reports_missing_openai_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(api_main, "DB_DIR", Path("."))
    monkeypatch.setattr(api_main, "load_ready_vectorstore", lambda: object())

    client = TestClient(api_main.app)

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "status": "unavailable",
            "checks": {
                "openai_api_key": False,
                "vectorstore_path": True,
                "vectorstore_loadable": True,
            },
        }
    }


def test_ready_endpoint_reports_missing_vectorstore_path(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(api_main, "DB_DIR", Path("__missing_ready_path__"))

    client = TestClient(api_main.app)

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "status": "unavailable",
            "checks": {
                "openai_api_key": True,
                "vectorstore_path": False,
                "vectorstore_loadable": False,
            },
        }
    }


def test_ready_endpoint_reports_vectorstore_load_failure(monkeypatch):
    def fail_to_load_vectorstore():
        raise RuntimeError("cannot load vectorstore")

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(api_main, "DB_DIR", Path("."))
    monkeypatch.setattr(api_main, "load_ready_vectorstore", fail_to_load_vectorstore)

    client = TestClient(api_main.app)

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "status": "unavailable",
            "checks": {
                "openai_api_key": True,
                "vectorstore_path": True,
                "vectorstore_loadable": False,
            },
        }
    }
