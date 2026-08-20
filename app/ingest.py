from dotenv import load_dotenv

from app.config import RESET_VECTORSTORE_ON_INGEST
from app.splitter import split_documents
from app.text_loaders import load_documents
from app.vectorstore import create_vectorstore, deduplicate_documents


def main():
    load_dotenv()

    documents = load_documents()
    print(f"Loaded {len(documents)} documents")

    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    unique_chunks = deduplicate_documents(chunks)
    print(f"Deduplicated to {len(unique_chunks)} chunks")

    create_vectorstore(unique_chunks, reset=RESET_VECTORSTORE_ON_INGEST)
    print("Vector database created successfully")


if __name__ == "__main__":
    main()
