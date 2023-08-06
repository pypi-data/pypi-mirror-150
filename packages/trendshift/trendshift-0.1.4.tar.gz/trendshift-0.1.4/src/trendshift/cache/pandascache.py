"""
pd_cache is a decorator for functions to cache the results of every call.

Other caching decorators like functools.lru_cache does not support pandas
objects because they cannot be hashed by default.
"""
import pandas as pd
from pandas.core.util.hashing import hash_pandas_object


def pd_cache(func):
    memory = dict()

    def __hash(something):
        if isinstance(something, pd.Series) \
                or isinstance(something, pd.Index) \
                or isinstance(something, pd.DataFrame):
            return hash_pandas_object(something)
        else:
            return hash(something)

    def __tokenize(func_, *args, **kwargs):
        result = func_.__name__
        for index, arg in enumerate(args):
            result += str(index)
            result += str(__hash(arg))
        for key, value in enumerate(kwargs):
            result += str(__hash(key))
            result += str(__hash(value))
        return result

    def __is_a_cached(token):
        nonlocal memory
        return token in memory

    def __keep(token, result):
        nonlocal memory
        memory[token] = result

    def __cached(token):
        nonlocal memory
        return memory[token]

    def decorator(*args, **kwargs):
        token = __tokenize(func, *args, **kwargs)
        if not __is_a_cached(token):
            __keep(token, func(*args, **kwargs))
        return __cached(token)

    return decorator
