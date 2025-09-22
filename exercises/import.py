# python_scripts/01_import_data.py
import json
from db_connect import get_db

def import_data():
    db = get_db()
    collection = db["movies"]

    with open("/data/movies.json", "r") as f:
        data = json.load(f)

    if isinstance(data, dict):  # Ensure list
        data = [data]

    collection.insert_many(data)
    print(f"Inserted {len(data)} documents into 'movies' collection.")

if __name__ == "__main__":
    import_data()
