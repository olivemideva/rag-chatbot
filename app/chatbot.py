import requests

from app.config import OLLAMA_MODEL

from app.prompts import SYSTEM_PROMPT

from app.retriever import build_context


def generate_answer(query, top_k=5):

    context, docs = build_context(
        query=query,
        top_k=top_k
    )

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=query
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    answer = response.json()["response"]

    sources = []

    for doc in docs:

        sources.append(
            doc.metadata
        )

    return {
        "answer": answer,
        "sources": sources,
    }