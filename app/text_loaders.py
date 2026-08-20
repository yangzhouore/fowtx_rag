# Used to load the pdf files

from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.pdf import PyPDFLoader

from app.config import DATA_DIR


def load_documents(data_dir=DATA_DIR):

    """
    Load documents from the specified directory.
    """

    data_path = Path(data_dir)

    if not data_path.exists():
        raise FileNotFoundError(f"Data directory {data_path} does not exist.")
    
    loader = DirectoryLoader(
        # Used for testing with markdown files
        # str(DATA_TEST_DIR),
        # glob="**/*.md",
        # loader_cls=TextLoader,
        # loader_kwargs={"encoding": "utf-8"},
        # show_progress=True,
    
        # Used for production with pdf files
        str(data_path),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
        silent_errors=False,
    )

    documents = loader.load()

    if not documents:
        raise ValueError(f"No documents were loaded from {data_path}.")

    return documents
