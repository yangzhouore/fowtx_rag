from langchain_core.documents import Document

from app.splitter import split_documents


def test_split_documents_splits_text_and_preserves_metadata():
    text = "Alpha sentence. " * 120
    doc = Document(page_content=text, metadata={"source": "manual.pdf", "page": 4})

    chunks = split_documents([doc])

    assert len(chunks) > 1
    assert all(chunk.page_content for chunk in chunks)
    assert all(chunk.metadata["source"] == "manual.pdf" for chunk in chunks)
    assert all(chunk.metadata["page"] == 4 for chunk in chunks)
