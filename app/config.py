# Configuration file for FOWT RAG system
from pathlib import Path

DATA_DIR = Path("data/raw")
DATA_TEST_DIR = Path("data/raw/test")
DB_DIR = Path("data/chroma_db")
RESET_VECTORSTORE_ON_INGEST = False

COLLECTION_NAME = "fowt_rag_knowledge_base"

EMBEDDING_MODEL = "text-embedding-3-small"  
LLM_MODEL = "gpt-4o-mini"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

RETRIEVAL_K = 6
