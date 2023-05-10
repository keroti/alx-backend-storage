#!/usr/bin/env python3
"""
Function that defines a Cache class that can be used to store data in Redis.
"""
import redis
from typing import Union, Callable
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

def call_history(method):
    @wraps(method)
    def wrap(self, *args, **kwargs):
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)
        
        self._redis.rpush(inputs_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, result)
        
        return result
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
