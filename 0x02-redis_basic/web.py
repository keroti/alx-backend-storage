#!/usr/bin/env python3
'''
function to implement a get_page function
(prototype: def get_page(url: str) -> str:).
'''
from typing import Callable
import requests
import redis
from functools import wraps


redis_client = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """
    get a page content with cache and tracker
    """
    redis_client.set(f"cached:{url}", count)
    redis_client.incr(f"count:{url}")
    redis_client.setex(f"cached:{url}", 10, redis_client.get(f"cached:{url}"))
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
