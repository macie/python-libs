# -*- coding: utf-8 -*-
"""
Jinja2 template decorator unit tests.

"""
from mock import MagicMock, patch
import unittest

from utils.gae_jinja2_template import template


class TemplateTest(unittest.TestCase):
    """
    Jinja2 template decorator tests.

    """
    def setUp(self):
        self.request = MagicMock()
        self.request.response.headers = {}
        self.request.response.write.side_effect = lambda x: x
        self.request.jinja2.render_template = MagicMock(
            side_effect=lambda name, **context: '{}: {}'.format(name,
                                                                context))

    def test_empty_context(self):
        context, name = {}, 'testname'

        @template(name)
        def test_function(request):
            return context

        test_function(self.request)

        self.request.jinja2.render_template.assert_called_with(
            name, **context)
        self.request.response.write.assert_called_with(
            '{}: {}'.format(name, context))

    def test_dict_context(self):
        context, name = {'value': 'test'}, 'testname'

        @template(name)
        def test_function(request):
            return context

        test_function(self.request)

        self.request.jinja2.render_template.assert_called_with(
            name, **context)
        self.request.response.write.assert_called_with(
            '{}: {}'.format(name, context))

    def test_none_context(self):
        context, name = {}, 'testname'

        @template(name)
        def test_function(request):
            return

        test_function(self.request)

        self.request.jinja2.render_template.assert_called_with(
            name, **context)
        self.request.response.write.assert_called_with(
            '{}: {}'.format(name, context))

    @patch('logging.error', MagicMock())
    def test_non_dict_context(self):
        context, name = {}, 'testname'

        @template(name)
        def test_function(request):
            return 'non dict context'

        test_function(self.request)

        self.request.jinja2.render_template.assert_called_with(
            name, **context)
        self.request.response.write.assert_called_with(
            '{}: {}'.format(name, context))
