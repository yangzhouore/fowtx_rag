from langchain_core.documents import Document

from app.vectorstore import deduplicate_documents


def test_deduplicate_documents_removes_exact_duplicates_and_preserves_order():
    first = Document(page_content="Same content", metadata={"source": "a.pdf", "page": 0})
    duplicate = Document(page_content=" Same content ", metadata={"source": "a.pdf", "page": 0})
    second = Document(page_content="Different content", metadata={"source": "a.pdf", "page": 1})

    result = deduplicate_documents([first, duplicate, second])

    assert result == [first, second]


def test_deduplicate_documents_keeps_different_sources_or_pages():
    documents = [
        Document(page_content="Shared", metadata={"source": "a.pdf", "page": 0}),
        Document(page_content="Shared", metadata={"source": "a.pdf", "page": 1}),
        Document(page_content="Shared", metadata={"source": "b.pdf", "page": 0}),
    ]

    result = deduplicate_documents(documents)

    assert result == documents
