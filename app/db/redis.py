from redis_om import get_redis_connection


params = {
    'host': 'paste_your_host',
    'port': 'paste_your_port',
    'password': 'paste_your_password',
    'decode_responses': True
}

redis = get_redis_connection()