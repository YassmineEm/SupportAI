from utils import document_reader
from utils.langchain_client import vector_store, text_splitter

async def handle_document_upload(file):
    file_bytes = await file.read()
    try:
        content = document_reader.extract_text_from_file(file_bytes, file.filename)
    except Exception as e:
        return {"error": str(e)}

    
    docs = text_splitter.split_text(content)

    
    vector_store.add_texts(docs, metadatas=[{"source": file.filename}] * len(docs))

    return {"status": "Document uploaded with LangChain", "chunks": len(docs)}

