# app.py

# --------------------------------------------------------------------
#* Exercise 4: Building a Video Game Store API With Flask and MongoDB 
# Use Flask backend, MongoDB, Pymongo, and JSON format for all API's
# ---------------------------------------------------------------------

from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import json, os

app = Flask(__name__)
ROUTE = 5000;

# MongoDB connection
client = MongoClient("mongodb://mongo:27017/")
db = client["storeDB"]

# Collections
games = db["games"]
clients = db["clients"]

# APP
@app.route('/')
def home():
    return jsonify({"message": "Video Game Store API"})

#* ------------Helpers------------
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

def serialize_doc(doc):
    """Convert ObjectId fields to string for JSON serialization."""
    doc_copy = doc.copy()
    if "_id" in doc_copy:
        doc_copy["_id"] = str(doc_copy["_id"])
    return doc_copy


#*-----------Init DB------------
@app.route('/api/initDB/<string:collection>', methods=['GET'])
def populate_collections(collection):
    file_map = {
        "games": "data/games.json",
        "clients": "data/clients.json"
    }
    try:
        match collection:
            case "games":
                import_from_file(file_map["games"], games)
                print("populated games collection.")
                return jsonify({"message": "populated games collection."})
            case "clients":
                import_from_file(file_map["clients"], clients)
                print("populated clients collection.")
                return jsonify({"message": "populated clients collection."})

            case "all": 
                import_from_file(file_map["games"], games)
                import_from_file(file_map["clients"], clients)
                print("populated all collection.")
                return jsonify({"message": "populated all collections."})
            case _:
                print("Error [populate_collections]: Unknown collection.")
                return jsonify({"error": "Unknown collection."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cleanDB', methods=['GET'])
def cleanup(collection):
    db.drop_collection(collection)
    # print("[cleanup] Dropped 'movies' collection.")
    return

@app.route('/api/showDB/<string:collection>', methods=['GET'])
def show_collection(collection):
    coll = db[collection]
    docs = list(coll.find())
    # Convert ObjectId to string for JSON
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    return jsonify(docs)


#*------------API-----------




#? 1. CRUD (Create, Read, Update, Delete) operations

# Create: Add a new video game to the store's inventory. 

# Read: 
# Retrieve a list of all games in the inventory. 
# — Retrieve a single game by its unique identifier (ID) _ 

# Update: Modify the details of an existing game (C.g., cliange the or quantity). 


# Delete: Remove a game from the inventory. 





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
    app.run(host='0.0.0.0', port=ROUTE, debug=True)