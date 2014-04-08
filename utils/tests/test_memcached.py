# -*- coding: utf-8 -*-
"""
Memcached decorator unit tests.

"""
from mock import MagicMock, patch
import unittest

from google.appengine.ext import testbed

from utils.gae_memcached import memcached


class MemcachedTest(unittest.TestCase):
    """
    Memcached decorator tests.

    """
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_no_time(self):
        key, value = 'test_key', 'test value'

        @memcached(key)
        def test_function():
            return value
        result = test_function()

        self.assertEqual(result, value)

    def test_with_time(self):
        key, value = 'test_key', 'test value'
        time = 1

        @memcached(key, time)
        def test_function():
            return value
        result = test_function()

        self.assertEqual(result, value)

    @patch('logging.critical', MagicMock())
    @patch('google.appengine.api.memcache.set',
           MagicMock(return_value=None))
    def test_set_error(self):
        key, value = 'test_key', 'test value'

        @memcached(key)
        def test_function():
            return value
        result = test_function()

        self.assertEqual(result, value)
