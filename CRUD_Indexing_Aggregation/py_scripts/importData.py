# python_scripts/01_import_data.py
import json, os
from db_connect import get_db, cleanup


def importFromJson():
    cleanup(False)
    movies = get_db()["movies"]
    file_path = os.path.join(os.path.dirname(__file__), "../data/movies.json")

    with open(file_path, "r") as file:
        data = json.load(file)   #import json
        movies.insert_many(data)
        print("Inserted JSON into DataBase.")
        # showDB()


if __name__ == "__main__":
    importFromJson()
