# python_scripts/99_cleanup.py
from db_connect import get_db

def cleanup():
    db = get_db()
    db.drop_collection("movies")
    print("Dropped 'movies' collection.")

if __name__ == "__main__":
    cleanup()
