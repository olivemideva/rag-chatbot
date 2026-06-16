import os

from sqlalchemy import text

from app.database import get_engine
from app.loaders import load_file, load_folder
from app.chunker import split_documents
from app.vector_store import add_documents

engine = get_engine()


def file_already_indexed(filename):

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT filename
                FROM indexed_files
                WHERE filename=:filename
                """
            ),
            {"filename": filename},
        ).fetchone()

    return result is not None


def mark_file_indexed(filename):

    with engine.begin() as conn:

        conn.execute(
            text(
                """
                INSERT INTO indexed_files(filename)
                VALUES(:filename)
                ON CONFLICT(filename)
                DO NOTHING
                """
            ),
            {"filename": filename},
        )


def ingest_file(file_path):

    filename = os.path.basename(file_path)

    if file_already_indexed(filename):

        return {
            "status": "skipped",
            "filename": filename,
            "reason": "Already indexed",
        }

    docs = load_file(file_path)

    chunks = split_documents(docs)

    add_documents(chunks)

    mark_file_indexed(filename)

    return {
        "status": "success",
        "filename": filename,
        "documents": len(docs),
        "chunks": len(chunks),
    }


def ingest_folder(folder_path):

    stats = []

    for file in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path):

            stats.append(
                ingest_file(file_path)
            )

    return stats