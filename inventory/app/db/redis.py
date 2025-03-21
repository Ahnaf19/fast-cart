from redis_om import get_redis_connection

params = {
    "host": "redis-12538.crce182.ap-south-1-1.ec2.redns.redis-cloud.com",
    "port": 12538,
    "password": "VyuFwaizfSL04uuWlWn3ch3xdDNoPsCz",
    "decode_responses": True,
}

redis_db = get_redis_connection(**params)
