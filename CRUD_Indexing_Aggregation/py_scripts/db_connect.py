# exercises/db_connect.py
from pymongo import MongoClient
import pprint
import json, os

client = MongoClient("mongodb://mongo:27017/")  # service name, not localhost
print("✅ Initial DB Connection...")


def get_db():
    return client["moviesdb"]

def get_movies_collection():
    return get_db()["movies"]

def showDB():
    """Prints all documents in the movies collection."""
    movies = get_movies_collection()
    all_movies = list(movies.find())
    
    if not all_movies:
        print("Database empty (movies collection).")
        return
    
    pprint.pprint(all_movies)


def cleanup(print):
    db = get_db()
    db.drop_collection("movies")
    if print : print("[cleanup] Dropped 'movies' collection.")
    showDB()


