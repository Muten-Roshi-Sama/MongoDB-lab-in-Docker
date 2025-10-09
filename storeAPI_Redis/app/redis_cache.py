# app/redis_cache.py
import json
import hashlib
import redis

# Simple defaults for docker-compose: Flask container can reach Redis at 'redis'
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0
DEFAULT_TTL = 5  # seconds

_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def make_list_key(collection: str, params: dict | None = None) -> str:
    if not params:
        return f"{collection}:list"
    qs = "&".join(f"{k}={params[k]}" for k in sorted(params))
    digest = hashlib.sha1(qs.encode("utf-8")).hexdigest()
    return f"{collection}:list:{digest}"

def make_id_key(collection: str, _id: str) -> str:
    return f"{collection}:{_id}"

def get_json(key: str):
    v = _client.get(key)
    if not v:
        return None
    try:
        return json.loads(v)
    except Exception:
        return None

def set_json(key: str, value, ex: int | None = None):
    _client.set(key, json.dumps(value, ensure_ascii=False), ex=(ex or DEFAULT_TTL))

def delete_key(key: str):
    return _client.delete(key)

def delete_pattern(pattern: str):
    deleted = 0
    for k in _client.scan_iter(match=pattern):
        deleted += _client.delete(k)
    return deleted