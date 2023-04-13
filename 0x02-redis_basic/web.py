#!/usr/bin/env python3
"""Module: Get Page"""
import requests
import redis
from functools import wraps
from datetime import timedelta
from typing import Callable
redis = redis.Redis()


def get_page_decorator(fn: Callable) -> Callable:
    """Decorates get_page"""
    @wraps(fn)
    def wrapper(*args, **kwargs) -> str:
        """Wrapped get_page"""
        url = args[0]
        key = "count:{}".format(url)
        if redis.get(key) is None:
            redis.setex(key, timedelta(seconds=10), 1)
        else:
            redis.incr(key)
        return fn(*args, **kwargs)
    return wrapper


@get_page_decorator
def get_page(url: str) -> str:
    """Gets a web page"""
    return requests.get(url, headers={"User-Agent": "Requests"}).content
