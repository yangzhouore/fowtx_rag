from dotenv import load_dotenv

from app.text_loaders import load_documents
from app.splitter import split_documents
from app.vectorstore import create_vectorstore


def main():
    load_dotenv()

    documents = load_documents()
    print(f"Loaded {len(documents)} documents")

    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    create_vectorstore(chunks)
    print("Vector database created successfully")


if __name__ == "__main__":
    main()