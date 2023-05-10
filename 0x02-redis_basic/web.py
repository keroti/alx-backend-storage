'''
function to implement a get_page function
(prototype: def get_page(url: str) -> str:).
'''
from functools import wraps
import uuid
import redis


def call_history(method):
    '''
    Function to store the history of inputs and outputs
    for a particular function
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, output)

        return output
    return wrapper


class Cache:
    """
    Class Cache.
    """

    def __init__(self):
        self._redis = redis.Redis()

    @call_history
    def store(self, value):
        """
        Generates a random key, stores the input(redis data) using the key
        and return it.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, value)
        return key
