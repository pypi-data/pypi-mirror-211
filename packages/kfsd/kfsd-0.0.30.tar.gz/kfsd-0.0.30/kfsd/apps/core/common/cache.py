from django.core.cache import cache as DjangoCache
from functools import wraps


def cache(key):
    def get(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return DjangoCache.get_or_set(key, func(*args, **kwargs), timeout=3600)

        return wrapper

    return get
