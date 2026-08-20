from langchain_core.documents import Document

from app.query import format_doc, format_docs, summarize_sources


def test_format_doc_includes_source_and_one_indexed_page():
    doc = Document(
        page_content="Floating platform text.",
        metadata={"source": "report.pdf", "page": 2},
    )

    assert format_doc(doc) == "Source: report.pdf, page 3\nFloating platform text."


def test_format_doc_uses_defaults_for_missing_metadata():
    doc = Document(page_content="No metadata text.", metadata={})

    assert format_doc(doc) == "Source: unknown\nNo metadata text."


def test_format_docs_joins_formatted_documents():
    docs = [
        Document(page_content="First", metadata={"source": "a.pdf", "page": 0}),
        Document(page_content="Second", metadata={"source": "b.pdf", "page": 1}),
    ]

    assert format_docs(docs) == "Source: a.pdf, page 1\nFirst\n\nSource: b.pdf, page 2\nSecond"


def test_summarize_sources_deduplicates_sources_in_order():
    docs = [
        Document(page_content="First", metadata={"source": "a.pdf", "page": 0}),
        Document(page_content="Duplicate", metadata={"source": "a.pdf", "page": 0}),
        Document(page_content="Missing page", metadata={"source": "b.pdf"}),
    ]

    assert summarize_sources(docs) == ["a.pdf (page 1)", "b.pdf (page unknown)"]
