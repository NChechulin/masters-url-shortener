import redis

redis_client = redis.Redis(host="redis_url", port=6379, db=0, decode_responses=True)
