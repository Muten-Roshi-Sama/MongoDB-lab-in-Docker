"""
Manual usage:
1. docker compose up
2. pytest -s        ←  IMPORTANT to see prints
"""
import requests, json
import pytest

BASE = "http://localhost:5000/api"



def test_full_manual():
    # print = lambda *args: print(*args)   # keep output
    # 1. seed
    r = requests.get(f"{BASE}/cleanDB/games")
    print("cleanDB", r.status_code, r.text[:80])
    r = requests.get(f"{BASE}/initDB/games")
    print("initDB ", r.status_code, r.text[:80])

    # 2. add
    payload = {
        "item": "Zelda Test",
        "price": 59.99,
        "quantity": 10,
        "genre": ["Adventure"],
        "platforms": ["Switch"],
        "release_year": 2017,
        "publisher": "Nintendo"
    }
    r = requests.post(f"{BASE}/add/games", json=payload)
    print("add    ", r.status_code, r.json())

    # 3. list
    r = requests.get(f"{BASE}/showDB/games")
    print("list   ", r.status_code, len(r.json()))

    # 4. update
    gid = r.json()[-1]["_id"]
    r = requests.put(f"{BASE}/update/games/{gid}?field=_id", json={"price": 39.99})
    print("update ", r.status_code, r.json())

    # 5. delete
    r = requests.delete(f"{BASE}/delete/games/{gid}?field=_id")
    print("delete ", r.status_code, r.json())







# ---------- pretty console ----------
# def pprint(json_obj):
#     print(json.dumps(json_obj, indent=2, ensure_ascii=False))

# # ---------- auto-seed ----------
# @pytest.fixture(scope="session", autouse=True)
# def seed():
#     print("\n=== Seeding games collection ===")
#     r = requests.get(f"{BASE}/cleanDB/games")
#     print("cleanDB:", r.json())
#     r = requests.get(f"{BASE}/initDB/games")
#     print("initDB :", r.json())

# # ---------- helpers ----------
# def add_game(payload: dict):
#     print(f"\n--- POST /add/games ---")
#     print("payload:", payload)
#     r = requests.post(f"{BASE}/add/games", json=payload)
#     print("status :", r.status_code, r.reason)
#     print("resp   :", r.json())
#     assert r.status_code == 201, r.text
#     return r.json()["id"]

# def update_game(gid: str, updates: dict):
#     url = f"{BASE}/update/games/{gid}?field=_id"
#     print(f"\n--- PUT {url} ---")
#     print("updates:", updates)
#     r = requests.put(url, json=updates)
#     print("status :", r.status_code)
#     print("resp   :", r.json())
#     assert r.status_code == 200
#     return r

# # ---------- tests ----------
# def test_add_game():
#     payload = {
#         "item": "Manual Pytest Game",
#         "price": 39.99,
#         "quantity": 7,
#         "genre": ["Arcade"],
#         "platforms": ["PC"],
#         "release_year": 2025,
#         "publisher": "TestCo"
#     }
#     gid = add_game(payload)
#     print("✅ _id =", gid)

# def test_get_game_by_id():
#     gid = add_game({"item": "ById", "price": 1, "quantity": 1,
#                     "genre": [], "platforms": [], "release_year": 2000,
#                     "publisher": "x"})
#     print(f"\n--- GET /get/games/{gid} ---")
#     r = requests.get(f"{BASE}/get/games/{gid}")
#     print("status:", r.status_code)
#     pprint(r.json())
#     assert r.status_code == 200
#     assert r.json()["item"] == "ById"

# def test_get_game_by_field():
#     add_game({"item": "ByField", "price": 2, "quantity": 2,
#               "genre": [], "platforms": [], "release_year": 2001,
#               "publisher": "x"})
#     print(f"\n--- GET /get/games/ByField?field=item ---")
#     r = requests.get(f"{BASE}/get/games/ByField?field=item")
#     print("status:", r.status_code)
#     pprint(r.json())
#     assert r.status_code == 200
#     assert r.json()["item"] == "ByField"

# def test_update_game():
#     gid = add_game({"item": "ToUpdate", "price": 10, "quantity": 10,
#                     "genre": [], "platforms": [], "release_year": 2002,
#                     "publisher": "x"})
#     update_game(gid, {"price": 77.77})
#     print(f"\n--- GET /get/games/{gid}  (after update) ---")
#     r = requests.get(f"{BASE}/get/games/{gid}")
#     pprint(r.json())
#     assert r.json()["price"] == 77.77

# def test_delete_game():
#     gid = add_game({"item": "ToDelete", "price": 3, "quantity": 3,
#                     "genre": [], "platforms": [], "release_year": 2003,
#                     "publisher": "x"})
#     print(f"\n--- DELETE /delete/games/{gid} ---")
#     r = requests.delete(f"{BASE}/delete/games/{gid}")
#     print("status:", r.status_code)
#     pprint(r.json())
#     r = requests.get(f"{BASE}/get/games/{gid}")
#     print("verify after delete:", r.status_code)  # expect 404
#     assert r.status_code == 404

# def test_list_games():
    # print(f"\n--- LIST /showDB/games  (after re-seed) ---")
    # requests.get(f"{BASE}/cleanDB/games")
    # requests.get(f"{BASE}/initDB/games")
    # for i in range(3):
    #     add_game({"item": f"List{i}", "price": i, "quantity": i,
    #               "genre": [], "platforms": [], "release_year": 2000,
    #               "publisher": "x"})
    # r = requests.get(f"{BASE}/showDB/games")
    # print("total games:", len(r.json()))
    # pprint(r.json()[:2])          # first 2 only
    # assert len(r.json()) == 3