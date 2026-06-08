import shutil

from langchain_chroma import Chroma

from app.config import DB_DIR, COLLECTION_NAME
from app.embeddings import get_embeddings


def deduplicate_documents(documents):
    seen = set()
    unique_documents = []

    for doc in documents:
        key = (
            doc.metadata.get("source"),
            doc.metadata.get("page"),
            doc.page_content.strip(),
        )

        if key in seen:
            continue

        seen.add(key)
        unique_documents.append(doc)

    return unique_documents


def reset_vectorstore():
    if DB_DIR.exists():
        shutil.rmtree(DB_DIR)


def create_vectorstore(documents, reset=False):
    """
    Create and persist a Chroma vector store from documents.
    """
    if reset:
        reset_vectorstore()

    embeddings = get_embeddings()
    unique_documents = deduplicate_documents(documents)

    return Chroma.from_documents(
        documents=unique_documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(DB_DIR),
    )


def load_vectorstore():
    """
    Load an existing Chroma vector store.
    """
    embeddings = get_embeddings()

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(DB_DIR),
    )
