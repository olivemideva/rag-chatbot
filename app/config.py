import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL Configuration

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Embedding Model

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Ollama Model

OLLAMA_MODEL = "llama3.2"

# Vector Store

COLLECTION_NAME = "rag_documents"

# Chunk Settings

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K = 5