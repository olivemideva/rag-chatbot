from app.vector_store import get_vector_store


def retrieve_documents(query, top_k=5):

    vector_store = get_vector_store()

    docs = vector_store.similarity_search(
        query,
        k=top_k
    )

    return docs


def build_context(query, top_k=5):

    docs = retrieve_documents(
        query=query,
        top_k=top_k
    )

    context = ""

    for i, doc in enumerate(docs):

        context += f"\n\n[Document {i+1}]\n"

        context += doc.page_content

    return context, docs