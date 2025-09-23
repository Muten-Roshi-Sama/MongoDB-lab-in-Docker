# exercises/db_connect.py
from pymongo import MongoClient
import pprint


def get_db():
    client = MongoClient("mongodb://mongo:27017/")  # service name, not localhost
    print("Connected to db.")
    return client["moviesdb"]


def showDB():
    """Prints all documents in the movies collection."""
    db = get_db()
    movies = db["movies"]
    all_movies = list(movies.find())
    
    if not all_movies:
        print("No movies in the database yet.")
        return
    
    pprint.pprint(all_movies)


def cleanup():
    db = get_db()
    db.drop_collection("movies")
    print("Dropped 'movies' collection.")
    showDB()