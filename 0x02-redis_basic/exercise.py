#!/usr/bin/env python3
"""
Function that defines a Cache class that can be used to store data in Redis.
"""
import redis
from typing import Union, Callable, Optional, List
from functools import wraps
import uuid
import functools


def count_calls(method: Callable) -> Callable:
    """
    function that takes a single method Callable argument and returns a Callable
    """
    key = method.__qualname__

    @functools.wraps(method)
    def wrap(self, *args, **kwargs):
        """
        function to increment count and call original method
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrap


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

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key, stores the input(redis data) using the key 
        and return it.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, List[str], List[bytes], List[int]]:
        """
        Get data and convert it using fn to format you want
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        data from Redis is converted back to a string
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        data from Redis is converted back to an integer
        """
        return self.get(key, int)


if __name__ == '__main__':
    cache = Cache()
