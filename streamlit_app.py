import os

import streamlit as st

from app.chatbot import generate_answer

from app.ingest import ingest_file

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 PostgreSQL RAG Chatbot")

st.markdown(
    """
Ask questions about:

- PDFs
- CSV files
- Excel files

Upload new files anytime.
"""
)

# -------------------
# SIDEBAR
# -------------------

with st.sidebar:

    st.header("Knowledge Base")

    top_k = st.slider(
        "Retrieved Documents",
        min_value=1,
        max_value=10,
        value=5,
    )

    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload PDF / CSV / Excel",
        type=["pdf", "csv", "xlsx"],
        accept_multiple_files=True,
    )

    if st.button("Upload & Index"):

        if uploaded_files:

            progress = st.progress(0)

            total = len(uploaded_files)

            for i, uploaded_file in enumerate(uploaded_files):

                save_path = os.path.join(
                    UPLOAD_FOLDER,
                    uploaded_file.name
                )

                with open(save_path, "wb") as f:

                    f.write(
                        uploaded_file.getbuffer()
                    )

                ingest_file(save_path)

                progress.progress(
                    (i + 1) / total
                )

            st.success(
                "Documents indexed successfully."
            )

        else:

            st.warning(
                "Select files first."
            )

# -------------------
# CHAT HISTORY
# -------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# -------------------
# CHAT INPUT
# -------------------

question = st.chat_input(
    "Ask a question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.spinner(
        "Searching knowledge base..."
    ):

        result = generate_answer(
            query=question,
            top_k=top_k,
        )

    answer = result["answer"]

    with st.chat_message("assistant"):

        st.markdown(answer)

        with st.expander(
            "Sources"
        ):

            for source in result["sources"]:

                st.write(source)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )