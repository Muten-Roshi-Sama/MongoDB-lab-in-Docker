# python_scripts/db_connect.py
from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://mongo:27017/")  # service name, not localhost
    print("Connected to db.")
    return client["moviesdb"]
