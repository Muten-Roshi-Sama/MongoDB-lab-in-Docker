
---

From : https://github.com/Muten-Roshi-Sama/MongoDB-lab-in-Docker

## 3. Store API Project + Redis

### Goals :
- Redis is an in-memory key-value store. It's blazingly fast and supports simple data structures.
- We’ll use it as a cache (not the source of truth): MongoDB remains authoritative.
- Good for read-heavy endpoints: list endpoints (/showDB/games) and single-doc endpoints (/get/games/:id).
- Basic flow: on GET, check Redis; if hit, return cached JSON. If miss, query Mongo, store JSON result in Redis with a TTL, then return it.
- On writes (POST/PUT/DELETE), invalidate affected keys so no stale data is returned.


### Parameters :
- TTL of 6 sec. (reduced from classic 120 sec. to 6 sec. to run pytest faster)

### What we added (Redis caching + pytest)

- Cache-aside strategy using Redis: the API checks Redis first for list and single-document responses. If a cached value exists it is returned immediately. On a cache miss the API queries MongoDB, stores the serialized JSON in Redis with a short TTL (default 120s), and then returns the response.
- Cache keys used by the implementation (simple, human-readable):
   - `<collection>:list` — cached JSON array for a full collection listing (e.g. `games:list`).
   - `<collection>:id:<_id>` — cached single-document responses by MongoDB _id (e.g. `games:id:64e...`).
   - When query parameters are involved the tests use a hashed key like `<collection>:list:<sha1(params)>` to keep list variants separate.
- Invalidation on writes: the API deletes affected keys when documents are added/updated/deleted so clients don't receive stale data.

### Why this is useful

- Speeds up read-heavy endpoints (list and single-item GETs) without changing MongoDB as the source of truth.
- Short TTL keeps data reasonably fresh while improving response time during bursts of reads.

### How to run the server and tests (recommended)

The repository includes both a Docker-based flow (recommended for parity with the lab) and a local development flow.

1) Using Docker Compose (recommended)

```powershell
cd "C:\Users\user\Desktop\ECAM\DataBase\X2\mongoDB_project\storeAPI_Redis"
docker compose up -d
```
This starts MongoDB, Redis, the Flask app container and optional helper services. Wait a few seconds for all services to become healthy.

2) Run pytest from the host (uses the running compose services)

```powershell
# Activate venv :
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run pytest (tests perform small API calls against the running compose services)
python -m pytest -q -s
```

Result :
```
(.venv) PS C:\Users\user\Desktop\ECAM\DataBase\X2\mongoDB_project\storeAPI_Redis> 
    
>>> python -m pytest -q -s


..=== Games Collection (8 items) ===
... and 6 more items
{
  "_id": "68e808ca5fef310fb7a1f8c6",
  "available": 35,
  "genre": ["FPS"],
  "item": "Black Ops 2",
  "platforms": ["PS3","PC","Xbox","WII"],
  "price": 29.99,
  "publisher": "Treyarch",
  "year": 2002
}

.COLD request time: 0.0085s, X-Cache=MISS
Redis key exists after cold request? True
HOT  request time: 0.0070s, X-Cache=HIT
HOT is 0.0015 seconds faster than COLD.

.Current TTL: 5
Waiting 6s for TTL to expire...
Exists after wait? False

Repopulated after request? True
.POST add time: 0.0094s, status=201
List cache exists after add? False

New id from POST: 68e808d05fef310fb7a1f8e6
New item present in list after repopulate? True
PUT update time: 0.0098s, status=200

List cache exists after update? False
GET single after update status: 200
Updated price: 9.99

DELETE time: 0.0092s, status=200
List cache exists after delete? False
.
6 tests passed in 7.19s
```

---

## Addendum: AI-assisted development notes

Development assisted by an AI pair-programmer: 
- manual test_routes.py migration to automated pytest, 
- Redis cache explanations (how it works + where to implement it), 
- helpers to verify TTL and invalidation, and 
- help when debugging. 

All AI suggestions were reviewed and applied by the developer (no auto-complete)
