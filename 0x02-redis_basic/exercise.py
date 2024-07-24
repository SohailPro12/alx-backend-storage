#!/usr/bin/env python3
"""
exercise.py module
"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    """Represents an object for storing data in a Redis data storage.
    """
    def __init__(self) -> None:
        """Initializes a Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """
        convert the data back to the desired format.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data
