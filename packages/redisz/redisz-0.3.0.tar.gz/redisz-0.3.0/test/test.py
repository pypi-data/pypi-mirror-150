import redis


def init_redis(url, **kwargs):
    if not url.lower().startswith(("redis://", "rediss://", "unix://")):
        url = 'redis://' + url

    connection_pool = redis.ConnectionPool.from_url(url, **kwargs)
    print(connection_pool)


# init_redis('127.0.0.1/3:6319')
# init_redis('127.0.0.1/3')
# init_redis('127.0.0.1:6379')
init_redis('localhost:6379', decode_responses=True)
