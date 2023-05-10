'''
function to implement a get_page function
(prototype: def get_page(url: str) -> str:).
'''
import requests
import redis
from functools import wraps

# create Redis client
redis_client = redis.Redis()


def track_calls(func):
    '''
    Function for tracking number of times a function is called
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        # increment count key for URL
        url = args[0]
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        # call wrapped function
        return func(*args, **kwargs)
    return wrapper


@track_calls
def get_page(url):
    """
    get a page content with cache and tracker
    """
    content = redis_client.get(url)
    if content is not None:
        return content.decode()
    # make request and store result in cache with expiration time
    response = requests.get(url)
    content = response.text
    redis_client.setex(url, 10, content)
    return content


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
