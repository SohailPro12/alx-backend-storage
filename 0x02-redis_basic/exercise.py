#!/usr/bin/env python3
"""
exercise.py module
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def replay(fn: Callable):
    """Display the history of calls of a particular function."""
    input_key = f"{fn.__qualname__}:inputs"
    output_key = f"{fn.__qualname__}:outputs"

    inputs = fn.__self__._redis.lrange(input_key, 0, -1)
    outputs = fn.__self__._redis.lrange(output_key, 0, -1)

    num_calls = len(inputs)

    print(f"{fn.__qualname__} was called {num_calls} times:")

    for input, output in zip(inputs, outputs):
        print(f"{fn.__qualname__}(*{input.decode('utf-8')},) ->
                {output.decode('utf-8')}")


def call_history(method: Callable) -> Callable:
    """
    track the inputs and the outputs of a function
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Returns output and input lists
        """
        In = '{}:inputs'.format(method.__qualname__)
        Out = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(In, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(Out, output)
        return output
    return invoker


def count_calls(method: Callable) -> Callable:
    """
     count how many times methods of the Cache class are called.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Invokes the given method after incrementing
        its call counter.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


class Cache:
    """Represents an object for storing data in a Redis data storage.
    """
    def __init__(self) -> None:
        """Initializes a Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
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

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from a Redis data storage.
        """
        return self.get(key, lambda x: int(x))
