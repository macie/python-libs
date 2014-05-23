# -*- coding: utf-8 -*-
"""
Memcache decorator for Google App Engine.

Maciej Żok, 2014 MIT License

"""
from functools import wraps
import logging
from google.appengine.api import memcache


class memcached(object):
    '''
    Sets/gets value from memcache.

    Args:
        key (str): Name of cache object
        time (datetime, optional): Expiration time (in seconds). By default
                                   item never expire.

    Returns:
        An object stored in memcache.

    Example:
        @classmethod
        @memcached('all_articles', time=3600)
        def get_all(cls):
            return ndb.get_multi(cls.query().iter(keys_only=True))

    '''
    def __init__(self, key, time=0):
        self.key = key
        self.time = time

    def __call__(self, cached_function):
        @wraps(cached_function)
        def get_from_memcache(*args, **kwargs):
            """
            Gets value from memcache or set it (if not exist).

            Returns:
                A cached value.

            """
            value = memcache.get(self.key)
            if not value:  # memcache object not exist
                value = cached_function(*args, **kwargs)
                if not memcache.set(self.key, value, self.time):
                    logging.critical("Setting memcache for <%r> failed!",
                                     self.key)
            return value
        return get_from_memcache
