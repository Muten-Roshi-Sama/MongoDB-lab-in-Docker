#  exercices/x2.py
from pymongo import MongoClient
import json, os
from db_connect import get_db, showDB, cleanup

#  ----------------------------------------------
#  DOCUMENTATION: https://pymongo.readthedocs.io/en/stable/api/index.html
# ----------------------------------------------------


db = get_db()
movies = db["movies"]   #Collection
cleanup()
showDB()

print("=== Examples of Indexing ===");

# The objective is to improve query performance by creating appropriate indexes. 
# Indexing allows to find a title immediatly against having to search through millions of titles.
#? always index fields that are frequently searched, filtered, or sorted.

#* 1. Using the movies collection from the previous exercise (or by recreating it), croate an index on the title field. 

# Create single index
res = movies.create_index("title")
print(f"Created Index: {res}")      # title_1


#* 2. Create a compound index on the year and genre fields to optimize search queries that combine these two criteria. 

# COMPOUND index (optimized for queries that use year+genre together.)
result = movies.create_index([("year", 1), ("genre", 1)])
print(f"Created compound index: {result}")      # year_1_genre_1
# Optimizes searches like this :
# movies.find({"year": {"$gte": 2000}, "genre": "Drama"})

# Prevents duplicate values.
# movies.create_index("title", unique=True)

# List all indexes
for idx in movies.list_indexes():
    print(idx)    # SON([('v', 2), ('key', SON([('year', 1), ('genre', 1)])), ('name', 'year_1_genre_1')])  
