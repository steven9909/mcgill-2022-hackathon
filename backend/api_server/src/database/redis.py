import redis
from typing import List

class RedisDb:
    def __init__(self):
        self.redis_conn = redis.Redis(
            host='127.0.0.1',
            port=6379, 
            password='WqZtbvXWQZZp'
        )
        
    def get_bodies(self, ids: List[int]):
        bodies = []
        for id in ids:
            bodies.append(self.redis_conn.lrange(id, 0, 4))
        return bodies
        