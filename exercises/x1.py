#  scripts/x1
from pymongo import MongoClient
from db_connect import get_db, showDB

db = get_db()
# cleanup()
movies = db["movies"]

print("=== Examples of CRUD operations ===");
showDB()

#* 2. Write
# Single insert
movies.insert_one({
    "title": " Inception " ,
    "director": " Christopher Nolan " ,
    "year": 2010 ,
    "genre": " Science Fiction " ,
    "actors": [" Leonardo DiCaprio " , " Joseph Gordon - Levitt " , " Elliot Page "]
    })
showDB()

# Multiple inserts
movies.insert_many([
    {
    "title": " Inception " ,
    "director": " Christopher Nolan " ,
    "year": 2010 ,
    "genre": " Science Fiction " ,
    "actors": [" Leonardo DiCaprio " , " Joseph Gordon - Levitt " , " Elliot Page "]
    },
    {
        "title": "The Godfather",
        "director": "Francis Ford Coppola",
        "year": 1972,
        "genre": "Crime",
        "actors": ["Marlon Brando", "Al Pacino", "James Caan"]
    }
])
showDB()


# Insert from .json





# //* 3. Search (Read) : 

# Find one
movie = movies.find_one({"title": "Inception"})
print(movie)

# Find all
for m in movies.find():
    print(m)

# Query with condition
for m in movies.find({"year": {"$gte": 2010}}):
    print(m)


#  Find the movie "Inception" 

#  Find all movics Of the genre " Thriller". 

#  Find all movics releascd after the year 2015. 

#  Find all movics in which " DiCaprio" has acted.

#  Find the movie The Godfather. 

#  Find all movics directed by Christopher Nolan. 

#  Find all movics in the gent. Science Fiction or Funtasy_ 

#  • Find all movie; released before the year 2000. 

#  • Find all movi«s released between 1990 and 21130 (inclusive). 

# Find all movie; in which Tom Hanks has acted. 



# Find all movics in which either Robert De Niro or Al Pacino has acted_ 
# Find all movics directed by Steven Spielbery after 1990. 
# Find all movics in the genre Druma releasod after the year 2000. 
# Find all movie; With more than two actors in the list. 
# • List all movies sorted by year (newest first). 
# • List Only the titles Of all Action movics. 


#* Update: 

# Update a single document
movies.update_one(
    {"title": "Inception"},   # filter
    {"$set": {"rating": 9.0}} # update
)

#  Update the "Parasite" movie document to add the genre "Black Comt%/y". 

# Update multiple documents
movies.update_many(
    {"genre": "Sci-Fi"},
    {"$set": {"sci_fi_fan_favorite": True}}
)

# Update the movie document to add the actor Tom Hardy" _ 



#* 5. Delctc: 
# Delete the "Inception" movie document.


