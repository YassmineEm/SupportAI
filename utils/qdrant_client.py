from qdrant_client import QdrantClient
from qdrant_client.http import models
import os

qdrant = QdrantClient(url=os.getenv("QDRANT_URL"))

# Create collection if it doesn't exist
try:
    collection_info = qdrant.get_collection("documents")
except Exception:
    # Create the collection with proper configuration
    qdrant.create_collection(
        collection_name="documents",
        vectors_config=models.VectorParams(
            size=1536,  # Dimension of text-embedding-ada-002 embeddings
            distance=models.Distance.COSINE
        )
    )