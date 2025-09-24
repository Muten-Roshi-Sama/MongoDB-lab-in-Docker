# app.py
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import json, os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://mongo:27017/")
db = client["storeDB"]

# Collections
games = db["games"]
clients = db["clients"]


#*-----------Init DB------------
def import_from_file(file_path, collection):
    """Import data from JSON file into specified collection"""
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return
    
    cleanup(collection)
    
    with open(full_path, "r", encoding='utf-8') as file:
        data = json.load(file)
        if data:  # Check if data is not empty
            collection.insert_many(data)
            print(f"Inserted {len(data)} documents into {collection.name} collection.")
        else:
            print(f"No data found in {file_path}")

def populate_collections(collection):
    match collection:
        case "games":
            import_from_file("../data/games.json", games)
            print("populated games collection.")
        case "clients":
            import_from_file("../data/clients.json", clients)
            print("populated clients collection.")

        case "all": 
            import_from_file("../data/games.json", games)
            import_from_file("../data/clients.json", clients)
            print("populated all collection.")

def cleanup(collection):
    db.drop_collection(collection)
    # print("[cleanup] Dropped 'movies' collection.")
    return



# ---------------------------------------------------------

#* Exercise 4: Building a Video Game Store API With Flask and MongoDB 
# Use Flask backend, MongoDB, Pymongo, and JSON format for all API's

#? 1. CRUD (Create, Read, Update, Delete) operations

# Create: Add a new video game to the store's inventory. 

# Read: 
# Retrieve a list of all games in the inventory. 
# — Retrieve a single game by its unique identifier (ID) _ 

# Update: Modify the details of an existing game (C.g., cliange the or quantity). 


# Delete: Remove a game from the inventory. 




# Vidco Game Storc Data Model 
# Before you begin coding, you will need to design your own data model for the different entities. Your 
# data model should include at least a gangs collection to store information about eacb video game and a 
# clients collection to store information about the clients of store Think about what information a 
# user would to know about a game, a client, etc. For example, you might include fields such as: 
# A unique identifier for cach game. 
# The title of the game. 
# The genre of the game. 
# The release year Of the game. 
# The platform(s) on whicA1 the game is available. 
# Gctting Startcd 
# Environment Setup: Croate a new project folder and eventually set up a Python virtual envi- 
# • Dependencies: Install Flask and PyMong01 using pip. 
# • Database Connection: Connect your Flask application to a local MongoDB instance or a cloud- 
# based service like MongoDB Atlas. 
# • API Endpoints: Define the Flask routes for cach Of the rC%1uircd CRUD operations. example, 
# a POST request to / api/ games could croate a new game, while a GET request to /api/ganes/ 
# would retrieve a specific game. 
# ht / h _ htm I fla
















#*------------API-----------
@app.route('/')
def home():
    return jsonify({"message": "Video Game Store API"})

@app.route('/api/games', methods=['GET'])
def get_all_games():
    """Get all games"""
    game_list = list(games.find())
    # Convert ObjectId to string for JSON serialization
    for game in game_list:
        game['_id'] = str(game['_id'])
    return jsonify(game_list)

@app.route('/api/games/<game_id>', methods=['GET'])
def get_game(game_id):
    """Get a specific game by ID"""
    try:
        game = games.find_one({"_id": ObjectId(game_id)})
        if game:
            game['_id'] = str(game['_id'])
            return jsonify(game)
        return jsonify({"error": "Game not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route('/api/games', methods=['POST'])
def add_game():
    """Add a new game"""
    new_game = request.get_json()
    result = games.insert_one(new_game)
    return jsonify({
        "message": "Game added successfully",
        "id": str(result.inserted_id)
    }), 201

@app.route('/api/games/<game_id>', methods=['PUT'])
def update_game(game_id):
    """Update a game"""
    try:
        updates = request.get_json()
        result = games.update_one(
            {"_id": ObjectId(game_id)},
            {"$set": updates}
        )
        if result.modified_count:
            return jsonify({"message": "Game updated successfully"})
        return jsonify({"error": "Game not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route('/api/games/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    """Delete a game"""
    try:
        result = games.delete_one({"_id": ObjectId(game_id)})
        if result.deleted_count:
            return jsonify({"message": "Game deleted successfully"})
        return jsonify({"error": "Game not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)