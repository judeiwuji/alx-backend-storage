#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
from uuid import uuid4
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable)\
        -> Callable:
    """A decorator function"""
    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        """A wrapper function"""
        obj = args[0]
        key = method.__qualname__
        redis = obj._redis

        if redis.get(key) == None:
            redis.set(key, 1)
        else:
            redis.incr(key)
        return method(*args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores function call history"""
    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        """Wrapper function"""
        key = method.__qualname__
        inputKey = "{}:inputs".format(key)
        outputKey = "{}:outputs".format(key)
        obj = args[0]
        redis = obj._redis
        input = str(args[1:])
        output = method(*args, **kwargs)
        redis.rpush(inputKey, input)
        redis.rpush(outputKey, str(output))
        return output
    return wrapper


class Cache:
    """An implemetation of a caching service"""

    def __init__(self):
        """Creates a new cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
