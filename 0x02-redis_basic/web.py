'''
function to implement a get_page function
(prototype: def get_page(url: str) -> str:).
'''
from functools import wraps
import requests
import redis


def call_history(method):
    '''
    Function to store the history of inputs and outputs
    for a particular function
    '''
    @wraps(method)
    def wrapper(*args, **kwargs):
        url = args[0]
        redis_client.incr(f"count:{url}")
        cached = redis_client.get(f'{url}')
        if cached:
            return cached.decode('utf-8')
        redis_client.setex(f'{url}, 10, {method(url)}')
        return method(*args, **kwargs)
    return wrapper


@call_history
def get_page(url: str) -> str:
    """get a page and cache value"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
