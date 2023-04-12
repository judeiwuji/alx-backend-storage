#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """An implemetation of a caching service"""

    def __init__(self):
        """Creates a new cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data to redis"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key
