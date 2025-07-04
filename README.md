# Chatbot API with FastAPI and LangChain

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.0.340-yellow.svg)
![Qdrant](https://img.shields.io/badge/Qdrant-1.1.1-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-0.27.6-purple.svg)

An intelligent document-based chatbot API powered by LangChain, featuring:
- Document processing and vector storage
- Context-aware question answering
- Chat transcript analysis

## Architecture Overview

![System Architecture](docs/architecture.png)

## Key Features

- **Document Processing**:
  - Supports PDF, DOCX, HTML, and TXT files
  - Automatic text extraction and chunking
  - Vector embeddings with OpenAI ADA-002
  - Storage in Qdrant vector database

- **Conversational AI**:
  - Retrieval-Augmented Generation (RAG) with LangChain
  - Contextual responses based on uploaded documents
  - GPT-4 powered answers

- **Analysis Tools**:
  - Automatic chat transcript evaluation
  - AI-generated feedback for support agents

## Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key
- Qdrant server
- MongoDB instance

### Installation
```bash
git clone https://github.com/YassmineEm/SupportAI.git
