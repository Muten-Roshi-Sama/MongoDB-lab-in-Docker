#  exercices/x3.py
from pymongo import MongoClient
import json, os
from db_connect import get_db, showDB, cleanup
from importData import importFromJson
#  ----------------------------------------------

db = get_db()
# print("Connected to db.")

movies = db["movies"]   #Collection

importFromJson()
# showDB()

print("=== Examples of Aggregation Pipelines ===");

# Exercise 3: Aggregation Pipeline 
# This exercise introduces you to the aggregation framework, a powerful tool for data analysis in MongoDB. 

# $match    : like SQL WHERE
# $group    : like SQL GROUP BY
# $project  : select/reshape fields
# $sort     : sort
# $limit    : pagination
# $skip     : pagination
# $lookup   : join collections
# $unwind   : flatten arrays


pipeline_group = [
    #* $sum : 
    #  accumulator in the aggregation framework: it adds up values for each group.
    #  {"$sum": 1}       : Count docs
    #  {"$sum": "$year"} : Adds up the year values of all docs in group
    #  {"$sum": {"$size": "$actors"}} : count total n° actors in all group

    # 1. COUNT ALL MOVIES
    {"$group": {"_id": None, "total_movies": {"$sum": 1}}},

    # 2. COUNT all movies in each genre
    {"$group": {"_id": "$genre", "count": {"$sum": 1}}},  

    # 3. AVG of release year per genre
    {"$group": {"_id": "$genre", "avg_year": {"$avg": "$year"}}},  

    # 4. FIND the earliest movie year per genre
    {"$group": {"_id": "$genre", "first_year": {"$min": "$year"}}},  

    # 5. FIND the latest movie year per genre
    {"$group": {"_id": "$genre", "last_year": {"$max": "$year"}}},  

    # 6. LIST all movie titles, grouped by director
    {"$group": {"_id": "$director", "movies": {"$push": "$title"}}},  

    # 7. LIST genres each actor has worked in (set removes duplicates)
    {"$group": {"_id": "$actors", "genres": {"$addToSet": "$genre"}}},  

    # 8. COUNT total number of actors across movies
    {"$group": {"_id": None, "total_actors": {"$sum": {"$size": "$actors"}}}},  

    # 9. AVG number of actors per genre
    {"$group": {"_id": "$genre", "avg_cast_size": {"$avg": {"$size": "$actors"}}}} 
]

pipeline_match = [
    #* same as .find()

    # 1.  FILTER select only Drama movies
    {"$match": {"genre": "Drama"}},

    # 2. Numeric comparison: movies released after 2015
    {"$match": {"year": {"$gt": 2015}}},  

    # 3. Multiple conditions (AND by default)
    {"$match": {"genre": "Action", "year": {"$gte": 2010}}},  

    # 4. Logical OR: Action movies OR movies after 2015
    {"$match": {"$or": [{"genre": "Action"}, {"year": {"$gt": 2015}}]}},  

    # 5. Text search with regex: titles starting with 'The'
    {"$match": {"title": {"$regex": r"^The"}}},  

    # 6. Array membership: movies where Leonardo DiCaprio acted
    {"$match": {"actors": "Leonardo DiCaprio"}},  

    # 7. Combining operators: Sci-Fi after 2010 or Fantasy after 2015
    {"$match": {"$or": [
        {"genre": "Science Fiction", "year": {"$gt": 2010}},
        {"genre": "Fantasy", "year": {"$gt": 2015}}
    ]}}


]

pipeline_project = [
    #* $project is used to reshape documents in a pipeline:
    # Include/exclude fields ,Rename fields, Compute new fields,  Apply expressions to existing fields
    # Think of it like SELECT in SQL: you decide what the output documents should contain
    # 0 : EXCLUDE field
    # 1 : INCLUDE

    
    # 1. Include only title and year
    {"$project": {"title": 1, "year": 1, "_id": 0}},  

    # 2. Include everything except _id
    {"$project": {"_id": 0}},  

    # 3. Rename a field: genre → movie_genre
    {"$project": {"title": 1, "movie_genre": "$genre", "_id": 0}},  

    # 4. Compute a new field: double the year
    {"$project": {"title": 1, "double_year": {"$multiply": ["$year", 2]}, "_id": 0}},  

    # 5. Get the number of actors per movie
    {"$project": {"title": 1, "num_actors": {"$size": "$actors"}, "_id": 0}},  

    # 6. Concatenate director and title into a new field
    {"$project": {"movie_info": {"$concat": ["$title", " by ", "$director"]}, "_id": 0}},  

    # 7. Conditional field: mark movie as recent if year > 2015
    {"$project": {"title": 1, "is_recent": {"$cond": [{"$gt": ["$year", 2015]}, True, False]}, "_id": 0}}  
]

pipeline_sort_limit_skip = [
    #  1 : ASCENDING
    # -1 : DESCENDING

    # SORT by year ascending
    {"$sort": {"year": 1}},

    # SORT by year ascending
    {"$sort": {"year": -1}},

    # SORT by genre ascending, then year descending
    # first field is primary, second is secondary
    {"$sort": {"genre": 1, "year": -1}},

    # ------LIMIT----------
    # get first 3 movies
    {"$limit": 3},
    #-------SKIP-----------
    # skip the first 2 movies
    {"$skip": 2}

]

pipeline_lookup = [
    #* COMBINE : 
    # documents from two collections based on a matching field.

]

pipeline_unwind = [
    #* flattens an array field, creating one document per array element
    # ex. for each actor, will output a new document
    # it EXPANDS arrays

    # 1. Simple unwind: flatten the actors array
    {"$unwind": "$actors"},  

    # 2. Unwind with index: keep track of actor position
    {"$unwind": {
        "path": "$actors",
        "includeArrayIndex": "actor_index"
    }},

    # # 3. Unwind + preserve empty arrays: keep movies with no actors
    {"$unwind": {
        "path": "$actors",
        "preserveNullAndEmptyArrays": True
    }},

    # # 4. Unwind after $lookup: each movie-review combination becomes one doc
    {"$lookup": {
        "from": "reviews",
        "localField": "title",
        "foreignField": "movie_title",
        "as": "reviews"
    }},
    {"$unwind": "$reviews"},  # now each review is a separate document
    {"$project": {"title": 1, "reviews.rating": 1, "_id": 0}},

    # # 5. Combine with $match: only keep reviews with rating > 8
    {"$unwind": "$reviews"},
    {"$match": {"reviews.rating": {"$gt": 8}}},
    {"$project": {"title": 1, "reviews": 1, "_id": 0}}

]

# res = list(movies.aggregate(pipeline_unwind))
# for m in res:
#     print(m)


#* --------Examples:--------

# -------Count all movies from after 2000 for each genre-------
pipeline = [
    {"$match": {"year": {"$gte": 2000}}},   # filter (WHERE)
    {"$group": {"_id": "$genre", "count": {"$sum": 1}}},  # COUNT all movies in each genre
    {"$sort": {"count": -1}}   # sort by count descending
]
# for m in list(movies.aggregate(pipeline)):
    # print(f' {m["_id"]} : {m["count"]}')


# -------Return 5 most Recent movies :-------
pipeline_pagination = [
    {"$sort": {"year":-1}},
    {"$skip": 0},   # skip first N
    {"$limit": 5}   # return 5
]
# res = list(movies.aggregate(pipeline_pagination))
# print(f"---5 most Recent movies :")
# for m in res:
#     print(f' {m["title"]}')


# -------Counts how many movies each actor appeared in.-------
pipeline = [
    {"$unwind": "$actors"},     # OUTPUT 1 doc for each actor
    {"$group": {"_id": "$actors", "movies_count": {"$sum": 1}}},  # SUM appearances
    {"$sort": {"movies_count": -1}}
]
# res = list(movies.aggregate(pipeline))
# for m in res:
#     print(f'{m["_id"]} : {m["movies_count"]}')


# -------Count documents-------
pipeline = [
    {"$match": {"genre": "Drama"}},
    {"$count": "total_dramas"}
]
# res = list(movies.aggregate(pipeline))
# print(f'Total Drama movies : {res[0]["total_dramas"]}')




#* Using the movios collection, build an aggregation pipeline for each of the following queries: 

# • Count the number of movies per genre and sort the results in descending Order by the number Of movies. 
pip = [
    {"$unwind" : "$genre"},
    {"$group" : {"_id": "$genre", "count": {"$sum":1}}},  # add $ to genre !!
    {"$sort": {"count": -1}}
]
# res = list(movies.aggregate(pip))
# for m in res:
#     print(f'{m["_id"]} : {m["count"]}')


# • Count the number of films by director: Find out which director the most films in the collection. 
pip = [
    {"$group" : {"_id" : "$director", "movies_made": {"$sum" : 1 }}},
    {"$sort": {"movies_made": -1}},
    {"$limit" : 1}
]
# res = list(movies.aggregate(pip))
# for m in res:
#     print(f'{m["_id"]} : {m["movies_made"]}')


# • Find the most prolific actor, that is, the one Who has appeared in the largest number of movies.
pip = [
    {"$group" : {"_id": "$actors", "appearances" : {"$sum": 1}}},
    {"$sort": {"appearances" : -1}},
    {"$limit": 1}
]
# res = list(movies.aggregate(pip))
# for m in res:
#     print(f'{m["_id"]} : {m["appearances"]}')

# Find films With more than three actors: Use the $project stage to calculate the size of the array and $match to filter based on that size. 
pip = [
    # {"$match": {"actors": {"$gt":3}}}
    {"$project": {
        "title": 1, 
        "actors": 1,
        "num_actors":{"$size":"$actors"}
    }},
    {"$match":{"num_actors":{"$gt":3}}}
]
res = list(movies.aggregate(pip))
for m in res:
    print(f'{m["title"]} : {m["num_actors"]} ({m["actors"]})')





