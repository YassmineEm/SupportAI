from qdrant_client import QdrantClient
from qdrant_client.http import models
import os

qdrant = QdrantClient(url=os.getenv("QDRANT_URL"))


try:
    collection_info = qdrant.get_collection("documents")
except Exception:
   
    qdrant.create_collection(
        collection_name="documents",
        vectors_config=models.VectorParams(
            size=1536,  
            distance=models.Distance.COSINE
        )
    )