#!/usr/bin/env python3
"""
Function that defines a Cache class that can be used to store data in Redis.
"""
from typing import Union, Callable
from functools import wraps
import uuid
import redis


class Cache:
    """
    Class Redis cache.
    """

    def __init__(self):
        """
        Initializes a new instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key, stores the input(redis data) using the key 
        and return it.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Get data and convert it using fn to format you want
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        data from Redis is converted back to a string
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        data from Redis is converted back to an integer
        """
        return self.get(key, fn=int)


if __name__ == '__main__':
    cache = Cache()
