import json
import logging
from typing import Optional

import redis
from config import REDIS_DB, REDIS_HOST, REDIS_KEY_TTL, REDIS_PORT

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self, *, connection=None):
        self.connection = connection or redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def set_key(self, key: str, value: dict) -> None:
        self.connection.set(key, json.dumps(value), ex=REDIS_KEY_TTL)

    def check(self, key: str) -> Optional[str]:
        value = self.connection.get(key)
        if value:
            return value.decode("utf-8")
        return None
