from qdrant_client import QdrantClient
import os

qdrant = QdrantClient(url=os.getenv("QDRANT_URL"))
