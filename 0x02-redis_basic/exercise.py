#!/usr/bin/env python3
""" Writes the class Cache """
import redis
import uuid
from typing import Union


def count_calls(method: Callable) -> Callable:
    """
        Decorator to track call count
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """
            adds its call count redis before execution
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to track args
    """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """
            tracks its passed argument by storing
            them to redis
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """
        Checks how many times a function was called and display:
    """
    client = redis.Redis()
    call = client.get(fn.__qualname__).decode('utf-8')

    inputs = [input.decode('utf-8') for input in
              client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]

    outputs = [output.decode('utf-8') for output in
               client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {call} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


class Cache:
    """
        this is a cache class
    """
    def __init__(self):
        """
            initialises the cache class

            :param self
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
             method should generate a random key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
            used to convert the data back to the desired format
        """
        if not self._redis.exists(key):
            return None

        data = self._redis.get(key)

        if not data:
            return
        if fn is int:
            return self.get_int(data)
        if fn is str:
            return self.get_str(data)
        if callable(fn):
            return fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        """ Converts bytes to string
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """ Converts bytes to integers
        """
        return int(data)
