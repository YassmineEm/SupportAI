from utils import db, qdrant_client, embedding_utils, document_reader
from qdrant_client.models import Distance, VectorParams
import uuid

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

    try:
       
        embedding = embedding_utils.generate_embedding(content)

        
        try:
            qdrant_client.qdrant.get_collection("documents")
        except Exception:
            qdrant_client.qdrant.create_collection(
                collection_name="documents",
                vectors_config=VectorParams(
                    size=1536,
                    distance=Distance.COSINE
                )
            )

      
        qdrant_client.qdrant.upsert(
            collection_name="documents",
            points=[{
                "id": str(uuid.uuid4()),  
                "vector": embedding,
                "payload": {
                    "filename": file.filename,
                    "mongo_id": str(doc_id), 
                    "content": content[:1000]
                }
            }]
        )

        return {"status": "Document uploaded", "id": str(doc_id)}

    except Exception as e:
        db.db.documents.delete_one({"_id": doc_id})
        return {"error": f"Failed to process document: {str(e)}"}
