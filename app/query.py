from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from app.config import LLM_MODEL, RETRIEVAL_K
from app.vectorstore import load_vectorstore

prompt = ChatPromptTemplate.from_template(
    """
Answer the question based only on the following context.

Context:
{context}

Question:
{question}
"""
)


def format_doc(doc):
    source = doc.metadata.get("source", "unknown")
    page = doc.metadata.get("page")
    page_label = f", page {page + 1}" if isinstance(page, int) else ""
    return f"Source: {source}{page_label}\n{doc.page_content}"


def format_docs(docs):
    return "\n\n".join(format_doc(doc) for doc in docs)


def summarize_sources(docs):
    seen = []

    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page")
        page_label = f"page {page + 1}" if isinstance(page, int) else "page unknown"
        item = f"{source} ({page_label})"

        if item not in seen:
            seen.append(item)

    return seen


def build_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": RETRIEVAL_K}
    )
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
    )

    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def answer_question(question):
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": RETRIEVAL_K}
    )
    retrieved_docs = retriever.invoke(question)
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
    )
    rag_chain = prompt | llm | StrOutputParser()
    answer = rag_chain.invoke(
        {
            "context": format_docs(retrieved_docs),
            "question": question,
        }
    )

    return {
        "answer": answer,
        "sources": summarize_sources(retrieved_docs),
    }


def main():
    load_dotenv()
    question = input("Question: ")
    result = answer_question(question)

    print("\nAnswer:")
    print(result["answer"])
    print("\nSources:")

    for item in result["sources"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()
