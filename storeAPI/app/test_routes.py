# test_routes.py
import requests
import json

HOST = "http://127.0.0.1:5000/api"


# ----------
#*  Helpers
# ----------

def showDB(collection, limit=None, fields=None):
    """
    Display collection contents with optional field filtering
    
    Args:
        collection: Collection name or "all" for all collections
        limit: Maximum number of items to display per collection
        fields: List of field names to display for each item (None = all fields)
    """
    res = requests.get(HOST + "/showDB/"+ collection)

    def _print_items(items, limit=None, fields=None):
        """Helper function to print items with field filtering"""
        items_to_show = items[:limit] if limit else items
        
        for i, item in enumerate(items_to_show):
            # Filter fields if specified
            if fields:
                filtered_item = {}
                for field in fields:
                    if field in item:
                        filtered_item[field] = item[field]
                    # Optional: include field with None if missing
                    # else:
                    #     filtered_item[field] = None
                print(json.dumps(filtered_item, indent=2))
            else:
                # Show all fields
                print(json.dumps(item, indent=2))
    
    # Show "more items" message if limited
    if limit and len(items) > limit:
        print(f"... and {len(items) - limit} more items")

    if res.status_code == 200:
        data = res.json()
        
        if collection == "all":
            # Handle the "all" case - data is a dictionary
            print(f"=== All Collections ===")
            for coll_name, items in data.items():
                print(f"--- {coll_name} ({len(items)} items) ---")
                _print_items(items, limit, fields)
        else:
            # Handle single collection - data is a list
            print(f"=== {collection.capitalize()} Collection ({len(data)} items) ===")
            _print_items(data, limit, fields)
    else:
        print(res.json().get('error', 'Unknown error'))


def sendRequest_get(command, collection, show=False):
    print(f"--- Testing /{command}/{collection} ---")
    response = requests.get(HOST + f"/{command}/{collection}")
    print(response.json())
    if show:
        showDB(collection, 4)
    return response

def add_instance(command, collection, show=False, json_data=None):
    print(f"--- POST /{command}/{collection} ---")
    response = requests.post(HOST + f"/{command}/{collection}", json=json_data)
    print(response.json())
    if show:
        showDB(collection, 4)
    return response    #["message"], response["id"]

def find_instance(collection, filter, value):
    print(f"--- POST /get/{collection} ---")

    if filter == "_id" :
        url = f"/get/{collection}/{filter}"

    else:
        url = f"/get/{collection}/{value}?field={filter}"
        
    print(f"URL: {url}")
    response = requests.get(HOST + url)
    print(response.json())

    return response

def update_instance(collection, field, value, updates):
    """Update instance by field value instead of ID"""
    encoded_value = requests.utils.quote(value)
    url = f"/update/{collection}/{encoded_value}?field={field}"
    
    print(f"--- PUT {url} ---")
    print(f"Updates: {json.dumps(updates, indent=2)}")
    
    response = requests.put(HOST + url, json=updates)
    
    if response.status_code == 200:
        print("✅ Update successful:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error {response.status_code}:")
        print(response.json())
    
    return response

# ----------
#*   Routes
# ----------
print("============================================")
print("============================================")

sendRequest_get("cleanDB", "all", False)
# showDB("all")


if True:
    # Init DB
    # sendRequest_get("initDB", "all", True)
    sendRequest_get("initDB", "games", False)
    # sendRequest_get("initDB", "clients", True)


    #?---------CRUD---------
    new_game = {
            "item": "The Legend of Zelda 2",
            "price": 99.99,
            "quantity": 19,
            "genre": ["Adventure"],
            "platforms": ["Nintendo Switch"],
            "release_year": 2017,
            "publisher": "Nintendo"
        }


    #----- Add
    add_instance("add", "games", False, new_game)

    #----- Read
    # showDB("games", 3)
    # showDB("clients", fields=["name", "_id", "bought"])
    # showDB("all", fields=["item", "_id", "price"])
    
    # find_instance("games","_id", "64b8f3f4e1b1f5e4d6c8b456")
    find_instance("games","item", "The Legend of Zelda 2")
    # find_instance("games","item", "willFail")
    # find_instance("games","genre", "Adventure")    #TODO: should find all

    # find_instance("clients","email", "sarah.johnson@gmail.com")
    # find_instance("clients","membership", "Gold") # TODO: find all who spent more than... joined before...


    #----- Update

    update_instance("games","item", "The Legend of Zelda 2", {
    "price": 54.99,
    "quantity": 0
    })

    find_instance("games","item", "The Legend of Zelda 2")




    #----- Delete
    # sendRequest_get("cleanDB", "all", True)
    # sendRequest_get("cleanDB", "games", True)
    # sendRequest_get("cleanDB", "clients", True) 




