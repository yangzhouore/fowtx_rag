from langchain_openai import OpenAIEmbeddings

from app.config import EMBEDDING_MODEL


def get_embeddings():
    """
    Create the OpenAI embedding model.
    """
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )