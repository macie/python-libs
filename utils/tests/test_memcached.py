# -*- coding: utf-8 -*-
"""
Memcached decorator unit tests.

"""
from mock import MagicMock, patch
import unittest

from utils.gae_memcached import memcached


class MemcachedTest(unittest.TestCase):
    """
    Memcached decorator tests.

    """
    @patch('google.appengine.api.memcache.get')
    def test_no_time_in_cache(self, memcache_mock):
        key, value = 'test_key', 'test value'
        memcache_mock.return_value = value

        @memcached(key)
        def test_function():
            return value

        result = test_function()

        self.assertEqual(result, value)

    @patch('google.appengine.api.memcache.get', MagicMock(return_value=None))
    @patch('google.appengine.api.memcache.set', MagicMock(return_value=True))
    def test_no_time_not_in_cache(self):
        key, value = 'test_key', 'test value'

        @memcached(key)
        def test_function():
            return value

        result = test_function()

        self.assertEqual(result, value)

    @patch('google.appengine.api.memcache.get')
    def test_with_time_in_cache(self, memcache_mock):
        key, value = 'test_key', 'test value'
        memcache_mock.return_value = value
        time = 1

        @memcached(key, time)
        def test_function():
            return value
        result = test_function()

        self.assertEqual(result, value)

    @patch('google.appengine.api.memcache.get', MagicMock(return_value=None))
    @patch('google.appengine.api.memcache.set', MagicMock(return_value=True))
    def test_with_time_not_in_cache(self):
        key, value = 'test_key', 'test value'
        time = 1

        @memcached(key, time)
        def test_function():
            return value
        result = test_function()

        self.assertEqual(result, value)

    @patch('logging.critical', MagicMock())
    @patch('google.appengine.api.memcache.get', MagicMock(return_value=None))
    @patch('google.appengine.api.memcache.set', MagicMock(return_value=None))
    def test_set_error(self):
        key, value = 'test_key', 'test value'

        @memcached(key)
        def test_function():
            return value
        result = test_function()

        self.assertEqual(result, value)
