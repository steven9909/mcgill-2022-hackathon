import redis
from typing import Tuple, List
import pickle

class RedisDb:
    def __init__(self):
        self.redis_conn = redis.Redis(
            host='127.0.0.1',
            port=6379, 
            password='WqZtbvXWQZZp'
        )
        
    def publish_next_bodies(self, bodies: List[Tuple]):
        for body in bodies:
            length = self.redis_conn.llen(body[0])
            
            if length == 0:
                self.redis_conn.lpush(body[0], body[1][0].item(), body[1][1].item(), body[2][0].item(), body[2][1].item())
            else:
                self.redis_conn.lset(body[0], 0, body[1][0].item())
                self.redis_conn.lset(body[0], 1, body[1][1].item())
                self.redis_conn.lset(body[0], 2, body[2][0].item())
                self.redis_conn.lset(body[0], 3, body[2][1].item())

    def publish_next_agents(self, agents: List[Tuple]):
        self.redis_conn.set("agents", pickle.dumps(agents))