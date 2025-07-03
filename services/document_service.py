from utils import db, qdrant_client, embedding_utils, document_reader

async def handle_document_upload(file):
    file_bytes = await file.read()
    try:
        content = document_reader.extract_text_from_file(file_bytes, file.filename)
    except Exception as e:
        return {"error": str(e)}

    document = {
        "filename": file.filename,
        "content": content
    }

    doc_id = db.db.documents.insert_one(document).inserted_id

    embedding = embedding_utils.generate_embedding(content)
    qdrant_client.qdrant.upsert(
        collection_name="documents",
        points=[
            {
                "id": str(doc_id),
                "vector": embedding,
                "payload": {"filename": file.filename}
            }
        ]
    )

    return {"status": "Document uploaded", "id": str(doc_id)}

