import redis


redis_client = redis.Redis(
    host="red-cvkopqadbo4c73f9jcr0:Wvl7YiEj0RxHfQpa5RHzAJttknNjooWR@frankfurt-keyvalue.render.com",
    port=6379,
    db=0,
    decode_responses=True,
)
