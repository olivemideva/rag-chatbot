import os
import json
import pandas as pd

from bs4 import BeautifulSoup

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
)

# Generic metadata creator

def create_document(content, source, **metadata):
    """
    Creates a LangChain Document.
    """

    meta = {
        "source": os.path.basename(source)
    }

    meta.update(metadata)

    return Document(
        page_content=str(content),
        metadata=meta
    )

# PDF

def load_pdf(file_path):

    loader = PyPDFLoader(file_path)

    return loader.load()

# CSV

def load_csv(file_path):

    loader = CSVLoader(file_path)

    return loader.load()

# Excel

def load_excel(file_path):

    df = pd.read_excel(file_path)

    docs = []

    for index, row in df.iterrows():

        docs.append(

            create_document(

                row.to_string(),

                file_path,

                row=index

            )

        )

    return docs

# Word

def load_word(file_path):

    loader = UnstructuredWordDocumentLoader(file_path)

    return loader.load()

# PowerPoint

def load_powerpoint(file_path):

    loader = UnstructuredPowerPointLoader(file_path)

    return loader.load()

# TXT / Markdown

def load_text(file_path):

    loader = TextLoader(file_path, encoding="utf-8")

    return loader.load()

# JSON

def load_json(file_path):

    with open(file_path, "r", encoding="utf-8") as f:

        data = json.load(f)

    return [

        create_document(

            json.dumps(data, indent=2),

            file_path

        )

    ]

# HTML

def load_html(file_path):

    with open(file_path, "r", encoding="utf-8") as f:

        soup = BeautifulSoup(f, "html.parser")

    text = soup.get_text(separator="\n")

    return [

        create_document(

            text,

            file_path

        )

    ]

# XML

def load_xml(file_path):

    with open(file_path, "r", encoding="utf-8") as f:

        content = f.read()

    return [

        create_document(

            content,

            file_path

        )

    ]

# Dispatcher

LOADERS = {

    ".pdf": load_pdf,

    ".csv": load_csv,

    ".xlsx": load_excel,

    ".xls": load_excel,

    ".docx": load_word,

    ".doc": load_word,

    ".pptx": load_powerpoint,

    ".txt": load_text,

    ".md": load_text,

    ".json": load_json,

    ".html": load_html,

    ".htm": load_html,

    ".xml": load_xml,

}

# Load one file

def load_file(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    loader = LOADERS.get(extension)

    if loader is None:

        print(f"Unsupported file type: {extension}")

        return []

    try:

        return loader(file_path)

    except Exception as e:

        print(f"Failed to load {file_path}")

        print(e)

        return []

# Load an entire folder

def load_folder(folder):

    documents = []

    if not os.path.exists(folder):

        return documents

    for root, _, files in os.walk(folder):

        for file in files:

            path = os.path.join(root, file)

            docs = load_file(path)

            documents.extend(docs)

    return documents