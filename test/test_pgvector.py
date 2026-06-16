from app.vector_store import get_vector_store

try:
    store = get_vector_store()

    print("PGVector initialized successfully")

except Exception as e:

    print("ERROR:")
    print(e)