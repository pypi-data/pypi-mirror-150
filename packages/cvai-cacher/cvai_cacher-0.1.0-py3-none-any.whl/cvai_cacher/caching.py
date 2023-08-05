from redis import Redis
from redis.exceptions import ConnectionError
from cvai_logger import hlogger


CACHING_PORT = 6379
LOCALHOST_CACHING_HOST = 'localhost'
CACHING_HOST = os.getenv('CACHING_HOST', LOCALHOST_CACHING_HOST)

redis_client = Redis(host=CACHING_HOST, port=CACHING_PORT)

def safe_cache(func):
    def inner(**kwargs):
        try:
            redis_client.ping()
            return func(**kwargs)
        except ConnectionError:
            hlogger.warning(f"Unable to ping redis client on {CACHING_HOST}:{CACHING_PORT}", code=None)
            return None
    return inner

@safe_cache
def set_cache(key, value):
    return redis_client.set(key, value)

@safe_cache
def get_cache(key):
    return redis_client.get(key)
