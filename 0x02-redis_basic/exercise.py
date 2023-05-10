#!/usr/bin/env python3
"""
Function that defines a Cache class that can be used to store data in Redis.
"""
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
