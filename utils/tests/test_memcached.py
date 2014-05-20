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
    @classmethod
    def setUpClass(cls):
        cls.memcache_get_patch = patch(
            'utils.gae_memcached.memcache.get',
            MagicMock())
        cls.memcache_get_mock = cls.memcache_get_patch.start()
        cls.memcache_get_mock.return_value = 'test value'

        cls.memcache_set_patch = patch(
            'utils.gae_memcached.memcache.set',
            MagicMock())
        cls.memcache_set_mock = cls.memcache_set_patch.start()
        cls.memcache_set_mock.return_value = True

    @classmethod
    def tearDownClass(cls):
        cls.memcache_get_patch.stop()
        cls.memcache_set_patch.stop()

    def test_no_time_in_cache(self):
        key, value = 'test_key', 'test value'

        @memcached(key)
        def test_function():
            return value

        result = test_function()

        self.assertEqual(result, value)

    def test_no_time_not_in_cache(self):
        self.memcache_get_mock.return_value = None
        key, value = 'test_key', 'test value'

        @memcached(key)
        def test_function():
            return value

        result = test_function()

        self.assertEqual(result, value)

    def test_with_time_in_cache(self):
        key, value = 'test_key', 'test value'
        time = 1

        @memcached(key, time)
        def test_function():
            return value
        result = test_function()

        self.assertEqual(result, value)

    def test_with_time_not_in_cache(self):
        self.memcache_get_mock.return_value = None
        key, value = 'test_key', 'test value'
        time = 1

        @memcached(key, time)
        def test_function():
            return value
        result = test_function()

        self.assertEqual(result, value)

    @patch('logging.critical', MagicMock())
    def test_set_error(self):
        self.memcache_set_mock.return_value = False
        key, value = 'test_key', 'test value'

        @memcached(key)
        def test_function():
            return value
        result = test_function()

        self.assertEqual(result, value)
