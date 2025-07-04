from utils.langchain_client import llm, vector_store
from langchain.chains import RetrievalQA

async def handle_chat(question: str):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

    answer = qa_chain.invoke({"query": question})

    return {"answer": answer["result"]}


