# Used to load the pdf files

from langchain_community.document_loaders import DirectoryLoader, TextLoader

from app.config import DATA_TEST_DIR

def load_documents():

    """
    Load documents from the specified directory.
    """

    if not DATA_TEST_DIR.exists():
        raise FileNotFoundError(f"Data directory {DATA_TEST_DIR} does not exist.")
    
    loader = DirectoryLoader(
        str(DATA_TEST_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    return loader.load()