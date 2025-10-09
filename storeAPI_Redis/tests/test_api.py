import os
import json
import time
import requests
import pytest

HOST = "http://127.0.0.1:5000/api"
TIMEOUT = 5 

#  --------- Notes ---------

# - Pytest fixtures: tell some functions to run before everysingle tests, or once at the start of the test session

# - URL encoding requests.utils.quote(value) makes weird string acceptable to be passed in a URL


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
    url = f"{HOST}/showDB/{collection}"
    res = requests.get(url, timeout=TIMEOUT)

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
            # Show "more items" message if limited
            if limit and len(data) > limit:
                print(f"... and {len(data) - limit} more items")
            _print_items(data, limit, fields)

    else:
        print(res.json().get('error', 'Unknown error'))

    return res




def sendRequest_get(command, collection, show=False):
    """Call GET /<command>/<collection> and return response"""
    # print(f"--- Testing /{command}/{collection} ---")
    url = f"{HOST}/{command}/{collection}"
    response = requests.get(url, timeout=TIMEOUT)
    # print(response.json())
    # if show:
    #     showDB(collection, 4)
    return response

def add_instance(collection, json_data=None, show=False):
    """POST /add/<collection> with provided JSON payload."""
    url = f"{HOST}/add/{collection}"
    response = requests.post(url, json=json_data, timeout=TIMEOUT)
    # print(response.json())
    # if show:
    #     showDB(collection, 4)
    return response    #["message"], response["id"]

def find_instance_by_field(collection, field, value):
    """GET /get/<collection>/<value>?field=<field>"""
    # print(f"--- POST /get/{collection} ---")
    url = f"/get/{collection}/{value}?field={field}"
    response = requests.get(HOST + url, timeout=TIMEOUT)
    return response

def get_instance_by_id(collection, _id):
    url = f"{HOST}/get/{collection}/{_id}"
    response = requests.get(url, timeout=TIMEOUT)
    return response

def update_instance(collection, field, value, updates):
    """Update instance by field value instead of ID"""
    encoded_value = requests.utils.quote(value)
    url = f"{HOST}/update/{collection}/{encoded_value}?field={field}"
    
    # print(f"--- PUT {url} ---")
    # print(f"Updates: {json.dumps(updates, indent=2)}")
    response = requests.put(url, json=updates, timeout=TIMEOUT)
    # if response.status_code == 200:
    #     print("✅ Update successful:")
    #     print(json.dumps(response.json(), indent=2))
    # else:
    #     print(f"❌ Error {response.status_code}:")
    #     print(response.json())
    
    return response

def delete_instance(collection, identifier, by_field=None):
    """
    Delete an instance from a collection
    
    Args:
        collection: Collection name (e.g., "games")
        identifier: ID or value to identify the instance
        by_field: Field to use for identification (None = use ID)
    """
    if by_field:
        # URL encode the identifier
        encoded_id = requests.utils.quote(identifier)
        url = f"/delete/{collection}/{encoded_id}?field={by_field}"
    else:
        url = f"/delete/{collection}/{identifier}"
    
    # print(f"--- DELETE {url} ---")
    
    response = requests.delete(HOST + url, timeout=TIMEOUT)
    
    # if response.status_code == 200:
    #     result = response.json()
    #     print("✅ Delete successful:")
    #     print(json.dumps(result, indent=2))
    # else:
    #     print(f"❌ Error {response.status_code}:")
    #     print(response.json())
    
    return response


# ------
# PYTESTS
# ------

@pytest.fixture(scope="session", autouse=True)   # scope makes it run once at start before anything else
def ensure_api():
    """Session-scoped fixture that waits for the API to become available.
    Embeds a small retry loop to avoid needing a separate helper function.
    """
    deadline = time.time() + 25.0
    url = HOST + "/"
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=TIMEOUT)
            if r.status_code in (200, 404):
                return True
        except requests.RequestException:
            pass
        time.sleep(0.5)
    pytest.exit(f"API not reachable at {HOST}. Start the API before running tests.")

@pytest.fixture(autouse=True)      # autouse makes it run before every single test to have a coherent state
def populate_db_collection(ensure_api):
    """
    Ensure a deterministic 'games' collection before each test by cleaning and re-initializing.
    This mirrors the manual flow you used in test_routes.py.
    """
    r = sendRequest_get("cleanDB", "games")
    # Accept 200 or 400 (if already absent) -- keep permissive
    assert r.status_code in (200, 400, 404)
    r = sendRequest_get("initDB", "games")
    assert r.status_code == 200
    yield
    # optional cleanup after each test to keep state tidy
    sendRequest_get("cleanDB", "games")


# ----------- TESTS -----------

def test_add_game_returns_id():
    new_game = {
        "item": "Zelda Test Simple",
        "price": 59.99,
        "available": 10,
        "genre": ["Adventure"],
        "platforms": ["Switch"],
        "year": 2017,
        "publisher": "Nintendo"
    }
    r = add_instance("games", new_game)
    assert r.status_code == 201, f"add returned: {r.status_code} {r.text}"
    body = r.json()
    assert "id" in body, f"expected id in response, got: {body}"

def test_full_crud_flow():
    # Add
    payload = {
        "item": "Zelda FullFlow",
        "price": 59.99,
        "available": 5,
        "genre": ["Adventure"],
        "platforms": ["Switch"],
        "year": 2017,
        "publisher": "Nintendo"
    }
    r_add = add_instance("games", payload)
    assert r_add.status_code == 201
    gid = r_add.json()["id"]

    # Read by id
    r_get = get_instance_by_id("games", gid)
    assert r_get.status_code == 200
    got = r_get.json()
    assert got["item"] == payload["item"]

    # Update by _id
    r_up = update_instance("games", "_id", gid, {"price": 39.99})
    assert r_up.status_code == 200
    r_get2 = get_instance_by_id("games", gid)
    assert r_get2.status_code == 200
    assert float(r_get2.json().get("price", 0)) == pytest.approx(39.99)

    # Delete by _id
    r_del = delete_instance("games", gid, by_field="_id")
    assert r_del.status_code == 200
    r_get3 = get_instance_by_id("games", gid)
    assert r_get3.status_code == 404

def test_show_and_search_helpers_work():
    # showDB
    r = showDB("games")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # find by field (use a known seed item name - adjust if your seed differs)
    r_search = find_instance_by_field("games", "item", "The Legend of Zelda")
    assert r_search.status_code in (200, 404)
    if r_search.status_code == 200:
        assert "item" in r_search.json()


