# -*- coding: utf-8 -*-
"""
Timezone unit tests.

"""
from datetime import datetime, timedelta, tzinfo
from mock import MagicMock, patch
import unittest

from utils.CET_timezone import CETTimeZone


class CETTimeZoneTest(unittest.TestCase):
    """
    CETTimeZone tests.

    """
    def test_init(self):
        stdoffset = timedelta(hours=1)
        reprname = 'Central European'
        stdname = 'CET'
        dstname = 'CEST'

        result = CETTimeZone()

        self.assertEqual(result.stdoffset, stdoffset)
        self.assertEqual(result.reprname, reprname)
        self.assertEqual(result.stdname, stdname)
        self.assertEqual(result.dstname, dstname)

    def test_repr(self):
        reprname = 'Central European'

        result = repr(CETTimeZone())

        self.assertEqual(result, reprname)

    def test_last_sunday_of_month(self):
        month, year = 5, 2012
        last_sunday = datetime(2012, 5, 27, 0, 0)

        result = CETTimeZone._CETTimeZone__last_sunday_of_month(year, month)

        self.assertEqual(result, last_sunday)

    @patch('utils.CET_timezone.CETTimeZone.dst',
           MagicMock(side_effect=lambda x: x))
    def test_tzname_dstname(self):
        tzname = 'CEST'
        is_dst = True

        result = CETTimeZone().tzname(is_dst)

        self.assertEqual(result, tzname)

    @patch('utils.CET_timezone.CETTimeZone.dst',
           MagicMock(side_effect=lambda x: x))
    def test_tzname_stdname(self):
        tzname = 'CET'
        is_dst = False

        result = CETTimeZone().tzname(is_dst)

        self.assertEqual(result, tzname)

    @patch('utils.CET_timezone.CETTimeZone.dst',
           MagicMock(side_effect=lambda x: timedelta(x)))
    def test_utcoffset(self):
        stdoffset = timedelta(hours=1)
        dst_offset = 0

        result = CETTimeZone().utcoffset(dst_offset)

        self.assertEqual(result, stdoffset)

    def test_dst_when_dt_is_none(self):
        dt = None
        offset = timedelta(hours=0)

        result = CETTimeZone().dst(dt)

        self.assertEqual(result, offset)

    def test_dst_when_dt_tzinfo_is_none(self):
        dt = MagicMock()
        dt.tzinfo = None
        offset = timedelta(hours=0)

        result = CETTimeZone().dst(dt)

        self.assertEqual(result, offset)

    def test_dst_when_not_dst(self):
        dt = datetime(2012, 1, 1, tzinfo=tzinfo())
        offset = timedelta(hours=0)

        result = CETTimeZone().dst(dt)

        self.assertEqual(result, offset)

    def test_dst_when_dst(self):
        dt = datetime(2012, 5, 12, tzinfo=tzinfo())
        offset = timedelta(hours=1)

        result = CETTimeZone().dst(dt)

        self.assertEqual(result, offset)
