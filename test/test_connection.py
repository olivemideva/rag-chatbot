from sqlalchemy import text
from app.database import get_engine

engine = get_engine()

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))

        print("Connected successfully!\n")

        print(result.fetchone()[0])

except Exception as e:
    print(e)