# test_routes.py
import requests
import json

BASE = "http://127.0.0.1:5000/api"


# ----------
#  Helpers
# ----------
def showDB(collection):
    res = requests.get(BASE + "/showDB/"+ collection)
    if res.status_code == 200:
        print("=== "+ collection.capitalize() + " Collection ===")
        for game in res.json():
            print(json.dumps(game, indent=2))
    else:
        print(res.json())


# showDB("games")
# showDB("clients")

# ----------
#   Routes
# ----------

# Init DB
collection = "clients"      # all, clients, games
# print(requests.get(BASE + "/initDB/" + collection).json())
# showDB("games")
# showDB("clients")

print("============================================")
# Clean up
# print(requests.delete(BASE + "/cleanDB/games").json())
print(requests.delete(BASE + "/cleanDB/clients").json())
showDB("clients")




# # Test root
# print(requests.get(BASE + "/").json())

# # Test movies
# print(requests.get(BASE + "/movies").json())
