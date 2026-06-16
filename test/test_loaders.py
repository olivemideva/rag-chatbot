from app.loaders import load_folder

docs = load_folder("data")

print(f"Loaded {len(docs)} documents")

for doc in docs[:5]:

    print("=" * 40)

    print(doc.metadata)

    print(doc.page_content[:200])