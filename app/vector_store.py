from langchain_postgres import PGVector

from app.config import (
    DATABASE_URL,
    COLLECTION_NAME,
)

from app.embeddings import get_embedding_model


def get_vector_store():
    """
    Returns the PGVector vector store.
    Automatically creates the collection if it does not exist.
    """

    embeddings = get_embedding_model()

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    return vector_store

def add_documents(documents):
    """
    Adds LangChain Document objects to PostgreSQL.
    """

    vector_store = get_vector_store()

    vector_store.add_documents(documents)