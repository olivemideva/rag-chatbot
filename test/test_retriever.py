from app.retriever import search_similar

query = "What are the course requirements?"

results = search_similar(query)

print("\nTop results:\n")

for i, r in enumerate(results):
    print(f"\nResult {i+1}")
    print("Content:", r["content"])
    print("Metadata:", r["metadata"])
    print("Distance:", r["distance"])