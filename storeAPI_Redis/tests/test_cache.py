import requests
import redis
import os
import pytest

HOST = os.environ.get("API_BASE", "http://127.0.0.1:5000/api")
r = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)

@pytest.fixture(autouse=True)
def setup():
    r.flushdb()
    requests.get(f"{HOST}/cleanDB/games")
    requests.get(f"{HOST}/initDB/games")
    yield
    r.flushdb()

def test_list_cache_hit():
    res1 = requests.get(f"{HOST}/showDB/games")
    assert res1.status_code == 200
    assert res1.headers.get("X-Cache") in (None, "MISS")
    res2 = requests.get(f"{HOST}/showDB/games")
    assert res2.status_code == 200
    assert res2.headers.get("X-Cache") == "HIT"

def test_add_invalidates_list_cache():
    requests.get(f"{HOST}/showDB/games")  # populate cache
    assert r.get("games:list") is not None
    payload = {"item":"RedisAdd","price":1.0,"available":1,"genre":[],"platforms":[],"year":2025,"publisher":"x"}
    rpost = requests.post(f"{HOST}/add/games", json=payload)
    assert rpost.status_code == 201
    assert r.get("games:list") is None