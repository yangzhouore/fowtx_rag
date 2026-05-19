# Used to load the pdf files

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders.pdf import PyPDFLoader

from app.config import DATA_TEST_DIR, DATA_DIR

def load_documents():

    """
    Load documents from the specified directory.
    """

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory {DATA_DIR} does not exist.")
    
    loader = DirectoryLoader(
        # Used for testing with markdown files
        # str(DATA_TEST_DIR),
        # glob="**/*.md",
        # loader_cls=TextLoader,
        # loader_kwargs={"encoding": "utf-8"},
        # show_progress=True,
    
        # Used for production with pdf files
        str(DATA_DIR),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
        silent_errors=True, 
    )

    return loader.load()