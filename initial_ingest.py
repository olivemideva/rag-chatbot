from app.ingest import ingest_folder

stats = ingest_folder("data")

for item in stats:

    print(item)