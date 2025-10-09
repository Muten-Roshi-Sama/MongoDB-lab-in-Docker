# app.py

# --------------------------------------------------------------------
#* Exercise 4: Building a Video Game Store API With Flask and MongoDB 
# Use Flask backend, MongoDB, Pymongo, and JSON format for all API's
# ---------------------------------------------------------------------

from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import json, os
import redis_cache 


app = Flask(__name__)
ROUTE = 5000

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

def collection_exists(collection_name):
    """Check if a collection exists in the database."""
    return collection_name in db.list_collection_names()

def get_collection_fields(collection_name):
    """Get ALL field names from existing documents in the collection"""
    try:
        collection = db[collection_name]
        
        # Get the first document to analyze its structure
        sample_doc = collection.find_one()
        
        if not sample_doc:
            # If collection is empty, return empty list or basic fields
            return []  # or return ['name', 'type'] if you want defaults
        
        # Return all field names except MongoDB internal fields
        all_fields = [key for key in sample_doc.keys() if key not in ['_id', '__v']]
        return all_fields
        
    except Exception as e:
        print(f"Error analyzing collection {collection_name}: {e}")
        return []  # Return empty list on error


#*-----------Init DB & Show------------
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



#*------------CRUD-----------
# 1. CRUD (Create, Read, Update, Delete) operations

#?----- Create: Add a new video game OR client.
@app.route('/api/add/<string:collection>', methods=['POST'])
def add_instance(collection):
    """Add a new video game to the store's inventory"""
    try:
        if not collection_exists(collection):
            return jsonify({"error": "Collection does not exist."}), 400

        new_data = request.get_json()
        
        # Get ALL fields that exist in this collection
        available_fields = get_collection_fields(collection)
        
        if not available_fields:
            # If collection is empty, we can't determine fields - accept anything
            target_collection = db[collection]
            result = target_collection.insert_one(new_data)
            
            # REDIS: Invalidate list caches and optionally cache the new item
            new_id = str(result.inserted_id)
            redis_cache.delete_pattern(f"{collection}:list*")
            redis_cache.set_json(redis_cache.make_id_key(collection, new_id), {**new_data, "_id": new_id})

            return jsonify({
                "message": f"Item added successfully to {collection} collection. (Collection was empty, so any fields accepted.)",
                "id": str(result.inserted_id),
                "item": {**new_data, "_id": str(result.inserted_id)}
            }), 201
        
        # Validate that at least some known fields are provided
        provided_fields = set(new_data.keys())
        known_fields = set(available_fields)
        
        # Check if any provided fields match the collection's known fields
        matching_fields = provided_fields.intersection(known_fields)
        
        if not matching_fields:
            return jsonify({
                "error": f"No recognized fields for {collection} collection",
                "available_fields": available_fields,
                "provided_fields": list(provided_fields)
            }), 400
        
        # Insert into the correct collection
        target_collection = db[collection]
        result = target_collection.insert_one(new_data)
        
        # REDIS: Invalidate list caches and cache new item (works for all collections)
        new_id = str(result.inserted_id)
        redis_cache.delete_pattern(f"{collection}:list*")
        redis_cache.set_json(redis_cache.make_id_key(collection, new_id), {**new_data, "_id": new_id})


        return jsonify({
            "message": f"Item added successfully to {collection} collection",
            "id": str(result.inserted_id),
            "item": {**new_data, "_id": str(result.inserted_id)},
            "available_fields": available_fields  # Return for reference
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500



#?----- Read: 
# Retrieve a list of all games in the inventory. 
@app.route('/api/showDB/<string:collection>', methods=['GET'])
def show_collection(collection):
    try:
        if collection == "all":
            if not db.list_collection_names(): #check if database contains at least one collection
                return jsonify({"error": "Database is empty..."}), 400
            
            # Create a dictionary to hold all collections
            all_data = {}
            
            for coll_name in db.list_collection_names():
                coll = db[coll_name]
                docs = list(coll.find())
                # Convert ObjectId to string for JSON
                for doc in docs:
                    doc["_id"] = str(doc["_id"])
                all_data[coll_name] = docs
            
            return jsonify(all_data)
        else:
            # Handle single collection (your existing code)
            if not collection_exists(collection):
                return jsonify({"error": "Collection does not exist."}), 400
            
            coll = db[collection]
            # build params dict from request args (if any)
            params = request.args.to_dict(flat=True) if request.args else None
            
            # REDIS: try cache for lists
            list_key = redis_cache.make_list_key(collection, params)
            cached = redis_cache.get_json(list_key)
            if cached is not None:
                resp = jsonify(cached)
                resp.headers['X-Cache'] = 'HIT'    # REDIS
                return resp
            
            # DB fallback and cache store
            docs = list(coll.find())
            for doc in docs:
                doc["_id"] = str(doc["_id"])
            
            redis_cache.set_json(list_key, docs)  # cache the list
            resp = jsonify(docs)
            resp.headers['X-Cache'] = 'MISS'
            return resp
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# — Find by unique identifier (ID) _ or ANY other field
@app.route('/api/get/<string:collection>/<path:lookup_value>', methods=['GET'])
def get_instance(collection, lookup_value):
    """Retrieve instance by ID or search across multiple fields"""
    try:
        if not collection_exists(collection):
            return jsonify({"error": f"Collection '{collection}' does not exist"}), 404

        target_collection = db[collection]
        
        # Try ObjectId search first
        if ObjectId.is_valid(lookup_value):
            # try cache first
            id_key = redis_cache.make_id_key(collection, lookup_value)
            cached = redis_cache.get_json(id_key)
            if cached is not None:
                resp = jsonify(cached)
                resp.headers['X-Cache'] = 'HIT'
                return resp
            
            # DB fallback   
            instance = target_collection.find_one({"_id": ObjectId(lookup_value)})
            if instance:
                instance["_id"] = str(instance["_id"])
                resp = jsonify(instance)
                resp.headers['X-Cache'] = 'MISS'
                return resp

        # If not found by ID or not an ObjectId, search by other fields
        field_name = request.args.get('field', None)
        
        if field_name:
            # Search by specific field
            search_query = {field_name: lookup_value}
            instance = target_collection.find_one(search_query)
        else:
            # Search across common text fields
            common_fields = get_collection_fields(collection)
            text_fields = [field for field in common_fields if isinstance(target_collection.find_one().get(field), str)]
            
            # Build OR query across all text fields
            or_conditions = [{field: lookup_value} for field in text_fields]
            if or_conditions:
                instance = target_collection.find_one({"$or": or_conditions})
            else:
                instance = None
        
        if instance:
            instance["_id"] = str(instance["_id"])
            return jsonify(instance)
        else:
            return jsonify({"error": f"No {collection} found matching: {lookup_value}"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500



#?---- Update: Modify the details of an existing game (C.g., cliange the or quantity). 
# update single
@app.route('/api/update/<string:collection>/<string:identifier>', methods=['PUT'])
def update_instance_by_field(collection, identifier):
    """Update instance by field value"""
    try:
        if not collection_exists(collection):
            return jsonify({"error": f"Collection '{collection}' does not exist"}), 404

        target_collection = db[collection]
        updates = request.get_json()
        field_name = request.args.get('field', 'name')  # Default to 'name'
        
        # Build filter query
        if field_name == '_id':
            if not ObjectId.is_valid(identifier):
                return jsonify({"error": "Invalid ID format"}), 400
            filter_query = {"_id": ObjectId(identifier)}
        else:
            filter_query = {field_name: identifier}
        
        # Update the instance
        result = target_collection.update_one(filter_query, {"$set": updates})
        
        if result.modified_count > 0:
            # REDIS: Invalidate relevant caches
                        # Invalidate caches for this collection
            redis_cache.delete_pattern(f"{collection}:list*")
            if field_name == '_id':
                # identifier is the id string
                redis_cache.delete_key(redis_cache.make_id_key(collection, identifier))
            else:
                # best-effort: find updated doc and delete its id cache
                try:
                    updated_doc = target_collection.find_one(filter_query)
                    if updated_doc and '_id' in updated_doc:
                        redis_cache.delete_key(redis_cache.make_id_key(collection, str(updated_doc['_id'])))
                except Exception:
                    pass
            
            return jsonify({"message": f"{collection.capitalize()} updated successfully"})
        else:
            return jsonify({"message": "No changes made or instance not found"})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update by 


#?---- Delete: 
# Remove a game from the inventory. 
@app.route('/api/delete/<string:collection>/<string:identifier>', methods=['DELETE'])
def delete_instance(collection, identifier):
    """Remove an instance by ID or field value"""
    try:
        if not collection_exists(collection):
            return jsonify({"error": f"Collection '{collection}' does not exist"}), 404

        target_collection = db[collection]
        
        # Determine if we're deleting by ID or by field
        field_name = request.args.get('field', None)
        
        if field_name == '_id' or not field_name:
            # Delete by ID
            if not ObjectId.is_valid(identifier):
                return jsonify({"error": "Invalid ID format"}), 400
            
            filter_query = {"_id": ObjectId(identifier)}
        else:
            # Delete by field value (delete first matching instance)
            filter_query = {field_name: identifier}
        
        # Check if instance exists
        instance = target_collection.find_one(filter_query)
        if not instance:
            return jsonify({"error": f"{collection.capitalize()} not found"}), 404
        
        # Delete the instance
        result = target_collection.delete_one(filter_query)
        
        if result.deleted_count > 0:
            # REDIS: Invalidate caches on delete
            if field_name == '_id':
                # identifier is the id string
                redis_cache.delete_key(redis_cache.make_id_key(collection, identifier))
            else:
                # use instance (found earlier) to remove item cache if possible
                try:
                    if instance and '_id' in instance:
                        redis_cache.delete_key(redis_cache.make_id_key(collection, str(instance['_id'])))
                except Exception:
                    pass
            redis_cache.delete_pattern(f"{collection}:list*")
            
            # Then return the existing success response
            instance["_id"] = str(instance["_id"])
            return jsonify({
                "message": f"{collection.capitalize()} deleted successfully",
                "deleted_instance": instance
            })
        else:
            return jsonify({"error": "Failed to delete instance"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500





# Remove ALL data from a collection, or all collections if "all" specified
@app.route('/api/cleanDB/<string:collection>', methods=['GET'])
def cleanup(collection):
    try:
        if collection == "all":
            for coll_name in db.list_collection_names():
                db.drop_collection(coll_name)
                print(f"[cleanup] Dropped '{coll_name}' collection.")
            return jsonify({"message": "Dropped all collections."})
        else:
            db.drop_collection(collection)
            print("[cleanup] Dropped 'movies' collection.")
            return jsonify({"message": f"Dropped '{collection}' collection."})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500





#------------------------- Run the app----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=ROUTE, debug=True)