from langchain_chroma import Chroma

from app.config import DB_DIR, COLLECTION_NAME
from app.embeddings import get_embeddings


def create_vectorstore(documents):
    """
    Create and persist a Chroma vector store from documents.
    """
    embeddings = get_embeddings()

    return Chroma.from_documents(
        documents=documents,
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