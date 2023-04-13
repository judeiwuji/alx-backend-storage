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
        if "Cache.{}".format(method.__name__) == method.__qualname__:
            self = args[0]
            key = method.__qualname__
            if self._redis.get(key) is None:
                self._redis.set(key, 1)
            else:
                self._redis.incr(key)
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
        self = args[0]
        input = str(args[1:])
        output = method(*args, **kwargs)
        self._redis.rpush(inputKey, input)
        self._redis.rpush(outputKey, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """Displays the call history of a particular
    function.

    Args:
        method(Callable)
    """
    obj = getattr(method, '__self__', None)
    redis = obj._redis
    key = method.__qualname__
    inputKey = "{}:inputs".format(key)
    outputKey = "{}:outputs".format(key)

    print("{} was called {:d} times:".format(key, int(redis.get(key))))
    for d in zip(redis.lrange(inputKey, 0, -1),
                 redis.lrange(outputKey, 0, -1)):
        print("{}(*{}) -> {}".format(key,
              d[0].decode('utf8'), d[1].decode('utf8')))


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

    def get(self, key: str, fn:
            Union[
                Callable[[bytes],
                         Union[str, bytes, int, float]], None] = None)\
            -> Union[str, bytes, int, float, None]:
        """Returns a stored data"""
        data = self._redis.get(key)
        if data is not None and fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes, int, float, None]:
        """Returns a stored data as string"""
        return self.get(key, str)

    def get_int(self, key: str) -> Union[str, bytes, int, float, None]:
        """Returns a stored data as int"""
        return self.get(key, int)
