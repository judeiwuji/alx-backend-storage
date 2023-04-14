#!/usr/bin/env python3
"""Module: Get Page"""
import requests
import redis
from functools import wraps
from datetime import timedelta
from typing import Callable
redis = redis.Redis()


def get_page_decorator(fn: Callable[[str], str]) -> Callable:
    """Decorates get_page"""
    @wraps(fn)
    def wrapper(*args, **kwargs) -> str:
        """Wrapped get_page"""
        url = args[0]
        if redis.get(f"count:{url}") is None:
            redis.setex(f"count:{url}", timedelta(seconds=10), 0)
        redis.incr(f"count:{url}")
        return fn(*args, **kwargs)
    return wrapper


@get_page_decorator
def get_page(url: str) -> str:
    """Gets a web page"""
    html = requests.get(url, headers={"User-Agent": "Requests"}).content
    return html
