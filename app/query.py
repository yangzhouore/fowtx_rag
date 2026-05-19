from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DB_DIR = "data/chroma_db"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings,
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

prompt = ChatPromptTemplate.from_template(
    """
Answer the question based only on the following context.

Context:
{context}

Question:
{question}
"""
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

question = input("Question: ")

answer = rag_chain.invoke(question)

print("\nAnswer:")
print(answer)