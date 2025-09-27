#  exercices/x1.py
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

print("=== Examples of CRUD operations ===");

#* 2. Write
# Single insert
# movies.insert_one({
#     "title": " Inception " ,
#     "director": " Christopher Nolan " ,
#     "year": 2010 ,
#     "genre": " Science Fiction " ,
#     "actors": [" Leonardo DiCaprio " , " Joseph Gordon - Levitt " , " Elliot Page "]
#     })
# # showDB()

# # Multiple inserts
# movies.insert_many([
#     {
#     "title": " Inception " ,
#     "director": " Christopher Nolan " ,
#     "year": 2010 ,
#     "genre": " Science Fiction " ,
#     "actors": [" Leonardo DiCaprio " , " Joseph Gordon - Levitt " , " Elliot Page "]
#     },
#     {
#         "title": "The Godfather",
#         "director": "Francis Ford Coppola",
#         "year": 1972,
#         "genre": "Crime",
#         "actors": ["Marlon Brando", "Al Pacino", "James Caan"]
#     }
# ])
# showDB()

# Test Cleanup
# cleanup()

#! ___________ Insert from .json ______________
file_path = os.path.join(os.path.dirname(__file__), "../data/movies.json")

with open(file_path, "r") as file:
    data = json.load(file)   #import json
    movies.insert_many(data)
    # showDB()



# //* 3. Search (Read) : 

#  Find the movie "Inception" 
res = movies.find_one({"title": "Inception"})   #only 1
movies.find({'title':"Inception"})               # find all
# print(f"Find one: {movie}")

# Find all -- showDB()
# print(f"Find all: {movie.find()}")

# Query with condition
# for m in movies.find({"year": {"$gte": 2010}}):
#     print(m)



#  Find all movics Of the genre " Thriller". 
movies.find({"genre":"Thriller"})


#  Find all movics released after the year 2015. 
res = movies.find({"year": {"$gt": 2018}})
print(f"Find all movics released after the year 2018:")
for m in res:
    # print(f"{m['title']} ({m['year']}) - directed by {m['director']}")
    print(f"{m.get('title', 'Unknown Title')} ({m.get('year', 'N/A')})") #hnadle missing cases

# Alternative to for - loop :
# print(f"Find all movics in the gent. Science Fiction or Funtasy_ : {movie}")
# --- can only print the full list of 



#  Find all movics in which " DiCaprio" has acted.
movies.find({'actors':"Leonardo DiCaprio"})

#  Find the movie The Godfather. 
movies.find({'title':"The Godfather"})

#  Find all movics directed by Christopher Nolan. 
movies.find({'director':"Christopher Nolan"})



#* FILTERING :

# { "<field>": { "$operator": <value> } }

#-------Comparison-------
# $eq : equal to (value)
# $ne : not equal to
# $gt : greater than
# $gte : greater than or equal
# $lt : lesser than ($lte)


#  • Find all movie; released before the year 2000. 
res = movies.find({"year": {"$lt": 2000}})

#  • Find all movi«s released between 1990 and 2000 (inclusive). 
res = movies.find({"year":{"$gte":1990}, "year":{"$lte":2000}})  #! No, 2d dict overwrites the 1st...
res = movies.find({"year":{"$gte":1990, "$lte":2000}})   #* <--- YES

# Find all movie; in which Tom Hanks has acted. 
res = movies.find({"actors": "Tom Hanks"})
res = movies.find({"actors":{"$eq": "Tom Hanks"}})  # SAME


#--------Logical operators-----
# $and :  movies.find({"$and": [{#1}, {#2}, ... ] }) #! only for different fields (ex. actor and genre)
# $or : either   (expects a list [...] )
# $nor : non of the conditions
# $in : membership (values in array)
# $nin : not in

#  Find all movics in the gent. Science Fiction or Funtasy_ 
res = list(movies.find({"genre": {"$in": ["Science Fiction", "Fantasy"]}}))

# Find all movics in which either Robert De Niro or Al Pacino has acted
res = movies.find({"actors": {"$in": ["Robert De Niro", "Al Pacino"]}})

# Find all movics directed by Steven Spielbery after 1990. 
res = movies.find({"director":"Steven Spielberg","year":{"$gt":1990}})

# Find all movics in the genre Drama releasod after the year 2000. 
res = movies.find({ "genre":"Drama", "year":{"$gt":2000} }) 

# Either Sci-Fi after 2015 OR Fantasy after 2010    #! $or expects a list [...]
movies.find({"$or": [
                {"genre":"Science Fiction", "year":{"$gt":2015}},
                {"genre":"Fantasy", "year":{"$gt":2010}}
                ]})

# ----------Array------------
# $all : 
# $size : array has exactly N elements

# All movies containing both
list(movies.find({"actors": {"$all": ["Leonardo DiCaprio", "Elliot Page"]}}))

# Movies with 3 actors listed
res = movies.find({"actors": {"$size":3}})

# • List Only the titles Of all Action movics. 
res = movies.find({"genre":"Action"})
for m in movies:
    print(m["Title"])



# -------Evaluation & Expressions -----------
# $expr:  aggregation expressions inside a query
# $regex: expression matching
# $mod: 
# $text:  text search (requires a text index):
# $where :

#----Example
#   { _id : 1, category : "food", budget : 400, spent : 450 },
#    { _id : 2, category : "drinks", budget : 100, spent : 150 },
# db.monthlyBudget.find( { $expr: { $gt: [ "$spent" , "$budget" ] } } )
#---- Find docswhere spent > budget


# titles starting with 'The '
list(movies.find({"title": {"$regex": r"^The\s"}}))  


# find docs where year > yearReleased+something OR compare fields:
res = list(movies.find({"$expr": {"$gt": ["$year", 2015]}}))

# Find all movies With more than two actors in the list. 
res = movies.find({"$expr": {"$gt":[{"$size": "$actors"}, 2]}})

#LOOP over entire db
for m in movies.find():
    if len(m["actors"]) > 2:
        print(m["title"])

# --------- SORT ----------
# • List all movies sorted by year (newest first). 
movies = movies.find().sort("year", -1)   #! descending (-1)
# Any other function applied like sort()






#* Update: 

# $set : set/overwrite a field
# $unset : Remove a field
# $push : add a value from an Array
# $pull : Remove a single value from an Array
# $inc : movies.update_one({"title": "Inception"}, {"$inc": {"rating": 1}} )


# Update a single document
movies.update_one(
    {"title": "Inception"},   # filter
    {"$set": {"rating": 9.0}} # update  (add or replace)
)

# Remove a single field
movies.update_one(
    {"title": "Inception"},
    {"$unset": {"rating": ""}}
)


#  Update the "Parasite" movie document to add the genre "Black Comedy".
movies.update_one(
    {"title": "Parasite"},
    {"$push": {"genre": "Black Comedy"}}
)

# Update the "Inception" movie document to add the actor Tom Hardy and Michael Caine" _ 
movies.update_one(
    {"title": "Inception"},
    {"$push": {"actors": {"$each": ["Tom Hardy", "Michael Caine"]}}}
)

# Remove a single value from an Array
movies.update_one({
    {"title": "Forrest Gump"},
    {"$pull": {"actors": "Tom Hanks"}}
})

# Update multiple documents 
movies.update_many(
    {"genre": "Sci-Fi"},
    {"$set": {"sci_fi_fan_favorite": True}}
)


#* 5. Delete: 

# Delete the "Inception" movie document.
movies.delete_one({"title":"Forret Gump"})

# Delete ALL based on criteria
movies.delete_many({"year": {"$lt": 2010}})


