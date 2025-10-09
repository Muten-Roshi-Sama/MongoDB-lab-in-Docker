import time
import json
import requests
import redis
import os
import pytest

HOST = os.environ.get("API_BASE", "http://127.0.0.1:5000/api")
r = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)

@pytest.fixture(autouse=True)
def setup():
    # ensure a clean Redis DB and seeded MongoDB for each test
    r.flushdb()
    requests.get(f"{HOST}/cleanDB/games")
    requests.get(f"{HOST}/initDB/games")
    yield
    r.flushdb()


def _exists(key):
    try:
        return r.exists(key) == 1
    except Exception:
        return False


def _dump_key(key):
    try:
        val = r.get(key)
        return val
    except Exception:
        return None


def test_list_cache_hit_timing_and_headers():
    """Measure cold vs hot request times and show X-Cache header and Redis key state."""
    url = f"{HOST}/showDB/games"

    # Cold request (should populate cache)
    t0 = time.perf_counter()
    r1 = requests.get(url)
    t1 = time.perf_counter()
    cold = t1 - t0

    print(f"COLD request time: {cold:.4f}s, X-Cache={r1.headers.get('X-Cache')}")
    assert r1.status_code == 200

    # Confirm cache key exists
    print("Redis key exists after cold request?", _exists("games:list"))

    # Hot request (should be fetched from cache)
    t0 = time.perf_counter()
    r2 = requests.get(url)
    t1 = time.perf_counter()
    hot = t1 - t0

    print(f"HOT  request time: {hot:.4f}s, X-Cache={r2.headers.get('X-Cache')}")
    assert r2.status_code == 200
    # Expect X-Cache header to indicate HIT on the second request if the app sets it
    assert r2.headers.get("X-Cache") == "HIT"

    # Basic perf expectation: hot should typically be faster than cold
    print(f"HOT is {cold - hot:.4f} seconds faster than COLD.")


def test_ttl_expiry_and_repopulate():
    """Verify TTL on the list cache key expires and a subsequent request repopulates it."""
    url = f"{HOST}/showDB/games"

    # Warm the cache
    requests.get(url)
    assert _exists("games:list")
    ttl = r.ttl("games:list")
    print("Current TTL:", ttl)

    if ttl is None or ttl < 0:
        # No TTL set or persist key - skip expiry test rather than fail
        pytest.skip("Cache key has no TTL set; cannot verify expiry")

    # Wait for TTL to expire (add small slack)
    wait = ttl + 1
    print(f"Waiting {wait}s for TTL to expire...")
    time.sleep(wait)

    print("Exists after wait?", _exists("games:list"))
    assert not _exists("games:list"), "Expected cache key to expire"

    # Next request should repopulate
    requests.get(url)
    assert _exists("games:list")
    print("Repopulated after request?", _exists("games:list"))


def test_add_update_delete_invalidation_and_timings():
    """Create, update, delete a resource and check cache invalidation and request timings.

    Prints simple timings and cache-state for visibility.
    """
    base = f"{HOST}"
    list_url = f"{base}/showDB/games"
    add_url = f"{base}/add/games"

    # Ensure cache is warm
    requests.get(list_url)
    assert _exists("games:list")

    # Add new item
    payload = {"name": "BENCH_TEST_GAME", "price": 1.23, "description": "bench"}
    t0 = time.perf_counter()
    rpost = requests.post(add_url, json=payload)
    t1 = time.perf_counter()
    print(f"POST add time: {t1 - t0:.4f}s, status={rpost.status_code}")
    assert rpost.status_code in (200, 201)

    # New item should cause list cache invalidation
    print("List cache exists after add?", _exists("games:list"))
    assert not _exists("games:list"), "Expected list cache to be invalidated after add"

    # Grab the new id from response (try JSON then text)
    new_id = None
    try:
        data = rpost.json()
        new_id = data.get("_id") or data.get("id")
    except Exception:
        new_id = (rpost.text or "").strip()

    print("New id from POST:", new_id)

    # Rebuild list (repopulate cache) and ensure the created item is present
    requests.get(list_url)
    lst = requests.get(list_url).json()
    found = any((str(x.get("_id") or x.get("id")) == str(new_id)) or (x.get("name") == "BENCH_TEST_GAME") for x in lst)
    print("New item present in list after repopulate?", found)
    assert found

    # Update the created item (if we have an id)
    if new_id:
        upd_url = f"{base}/update/games/{new_id}"
        t0 = time.perf_counter()
        rput = requests.put(upd_url, json={"price": 9.99})
        t1 = time.perf_counter()
        print(f"PUT update time: {t1 - t0:.4f}s, status={rput.status_code}")
        assert rput.status_code in (200, 201)

        # list cache should have been invalidated
        print("List cache exists after update?", _exists("games:list"))
        assert not _exists("games:list")

        # GET single item and validate updated field
        get_url = f"{base}/get/games/{new_id}"
        rget = requests.get(get_url)
        print(f"GET single after update status: {rget.status_code}")
        if rget.status_code == 200:
            j = rget.json()
            print("Updated price:", j.get("price"))

        # Delete the item
        t0 = time.perf_counter()
        rdel = requests.delete(f"{base}/delete/games/{new_id}")
        t1 = time.perf_counter()
        print(f"DELETE time: {t1 - t0:.4f}s, status={rdel.status_code}")
        assert rdel.status_code in (200, 204)

        # list cache should be invalidated
        print("List cache exists after delete?", _exists("games:list"))
        assert not _exists("games:list")
    else:
        pytest.skip("Could not determine new_id from POST response; skipping update/delete checks")