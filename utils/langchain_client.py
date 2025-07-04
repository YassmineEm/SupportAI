import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import Qdrant  # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY, temperature=0.5)

qdrant_client = QdrantClient(url=QDRANT_URL)
vector_store = Qdrant(client=qdrant_client, collection_name="documents", embeddings=embeddings)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
