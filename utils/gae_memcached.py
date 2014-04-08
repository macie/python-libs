# -*- coding: utf-8 -*-
"""
Memcache decorator for Google App Engine.

Maciej Żok, 2013 MIT License

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
        Object stored in memcache.

    Example:
        @classmethod
        @memcached('all_articles', time=3600)
        def get_all(cls):
            return ndb.get_multi(cls.query().iter(keys_only=True))

    '''
    def __init__(self, key, time=0):
        self.key = key
        self.time = time

    def __call__(self, f):
        @wraps(f)
        def get_from_memcache(*args, **kwargs):
            value = memcache.get(self.key)
            if not value:  # memcache object not exist
                value = f(*args, **kwargs)
                if not memcache.set(self.key, value, self.time):
                    logging.critical("Setting memcache for <%r> failed!",
                                     self.key)
            return value
        return get_from_memcache
