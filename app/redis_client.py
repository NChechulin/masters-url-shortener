import redis
from os import getenv


REDIS_HOST = getenv("REDIS_HOST", "redis_url")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)
