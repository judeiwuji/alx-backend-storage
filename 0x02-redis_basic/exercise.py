#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


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

    def get(self, key: str, fn: Callable[[bytes], Union[str, bytes, int, float]] = None)\
            -> Union[str, bytes, int, float, None]:
        """Returns a stored data"""
        data = self._redis.get(key)
        if data != None and fn != None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes, int, float, None]:
        """Returns a stored data as string"""
        return self.get(key, str)

    def get_int(self, key: str) -> Union[str, bytes, int, float, None]:
        """Returns a stored data as int"""
        return self.get(key, int)
