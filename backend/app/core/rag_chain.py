from typing import Dict, List, Tuple
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

from app.models.llm import get_llm_model
from app.core.vectorstore import get_vector_store
from app.config import NUM_DOCUMENTS

def create_rag_prompt() -> PromptTemplate:
    template = """
    You are a knowledgeable and helpful AI assistant. Your task is to answer the user's question using the context provided below. 
    Use only the information in the context to construct your response. If the context does not contain the answer, say you don’t know.

    Be concise, accurate, and focus only on the relevant information.

Context:
{context}

Question:
{query}

Answer:
"""
    return PromptTemplate.from_template(template.strip())


# Format documents for prompt
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Get retriever from vector store
def get_retriever(search_kwargs: Dict = None):
    if search_kwargs is None:
        search_kwargs = {"k": NUM_DOCUMENTS}
    vectorstore = get_vector_store()
    return vectorstore.as_retriever(search_kwargs=search_kwargs)

# Create basic RAG chain
def create_basic_rag_chain():
    llm = get_llm_model()
    retriever = get_retriever()
    prompt = create_rag_prompt()

    rag_chain = (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

# Unified query function
def query_rag_chain(query: str) -> Tuple[str, List[str]]:
    vectorstore = get_vector_store()
    docs = vectorstore.similarity_search(query, k=NUM_DOCUMENTS)
    sources = [doc.metadata.get("source", "") for doc in docs] 

    rag_chain = create_basic_rag_chain()
    answer = rag_chain.invoke(query)

    return answer, sources