#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
import redis
import time
from functools import wraps


redis_client = redis.Redis()


def count_access(fn):
    """
    Decorator to count accesses to a URL.
    """
    @wraps(fn)
    def wrapper(url):
        redis_client.incr(f"count:{url}")
        return fn(url)
    return wrapper


def cache_result(expiration=10):
    """
    cache the result of the function call.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(url):
            cached_page = redis_client.get(f"cached:{url}")
            if cached_page:
                return cached_page.decode('utf-8')
            result = fn(url)
            redis_client.setex(f"cached:{url}", expiration, result)
            return result
        return wrapper
    return decorator


@cound_access
@cache_result(expiration=10)
def get_page(url: str) -> str:
    """
    Fetch HTML content of a URL and cache it.
    """
    response = requests.get(url)
    return response.text
