from fastapi import FastAPI
from routes import document_routes, chat_routes, analyze_routes

app = FastAPI()

app.include_router(document_routes.router, prefix="/documents")
app.include_router(chat_routes.router, prefix="/chatbot")
app.include_router(analyze_routes.router, prefix="/analyze")
