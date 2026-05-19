# Configuration file for FOWT RAG system
from pathlib import Path

DATA_DIR = Path("data/raw")
DATA_TEST_DIR = Path("data/raw/test")
DB_DIR = Path("data/chroma_db")

COLLECTION_NAME = "fowt_rag_knowledge_base"

EMBEDDING_MODEL = "text-embedding-3-small"  

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

RETRIEVAL_K = 4
