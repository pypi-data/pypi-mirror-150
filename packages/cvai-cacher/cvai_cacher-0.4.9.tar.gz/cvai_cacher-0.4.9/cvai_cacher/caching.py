import os
import json
from redis import Redis, ConnectionPool
from redis.exceptions import ConnectionError
from cvai_logger import hlogger


CACHING_PORT = 6379
LOCALHOST_CACHING_HOST = 'localhost'
CACHING_HOST = os.getenv('CACHING_HOST', LOCALHOST_CACHING_HOST)

DEFAULT_EXP_TIME = 2 * 60 # 2 minutes

# conn_pool = ConnectionPool()
redis_client = Redis(host=CACHING_HOST, port=CACHING_PORT, socket_timeout=1)

def safe_cache(func):
    def inner(**kwargs):
        try:
            return func(**kwargs)
        except ConnectionError:
            hlogger.warning(f"Unable to ping redis client on {CACHING_HOST}:{CACHING_PORT}", code=None)
            return None
    return inner

@safe_cache
def set_cache(key, value, exp=DEFAULT_EXP_TIME):
    if type(value) == dict:
        value = json.dumps(value)
    res = redis_client.set(key, value, ex=exp)
    redis_client.expire(key, exp)
    return res

@safe_cache
def get_cache(key):
    result = redis_client.get(key)
    j = decode_result(result)
    return j

# multiple caches
@safe_cache
def get_mcache(keys):
    results = redis_client.mget(keys)
    js = map(lambda x: decode_result(x), results)
    return list(js)

def decode_result(result):

    # result not present in the DB
    if result == None:
        return result

    string = result.decode("utf-8")
    j = json.loads(string)

    return j
