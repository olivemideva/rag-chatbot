from app.chatbot import generate_answer

query = "Which sector is dominated by women?"

result = generate_answer(query)

print("\nANSWER:\n")
print(result["answer"])

print("\nSOURCES:\n")
for s in result["sources"]:
    print(s["metadata"])