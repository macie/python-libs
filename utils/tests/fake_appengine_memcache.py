# -*- coding: utf-8 -*-
"""
Fake google.appengine.api module.

"""


class memcache(object):
    """
    Fake memcache object.

    """
    @staticmethod
    def get(key):
        return 'value of {}'.format(key)

    @staticmethod
    def set(key, value, time):
        return True
