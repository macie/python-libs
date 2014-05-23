# -*- coding: utf-8 -*-
"""
Central European Time definition for datetime and time modules.

Maciej Żok, 2014 MIT License

"""
from datetime import datetime, timedelta, tzinfo


class CETTimeZone(tzinfo):
    """
    CET/CEST tzinfo object.

    Range of summer time (CEST):
        last sunday of March 01:00 UTC - last sunday of October 01:00 UTC

    Example:
        from datetime import datetime
        tz = CETTimeZone()
        local_time = datetime.now(tz)

    """
    def __init__(self):
        super(CETTimeZone, self).__init__()
        self.stdoffset = timedelta(hours=1)
        self.reprname = 'Central European'
        self.stdname = 'CET'
        self.dstname = 'CEST'

    def __repr__(self):
        return self.reprname

    def tzname(self, dt):
        if self.dst(dt):
            return self.dstname
        else:
            return self.stdname

    def utcoffset(self, dt):
        return self.stdoffset + self.dst(dt)

    def dst(self, dt):
        if dt is None or dt.tzinfo is None:
            return timedelta(hours=0)

        # summer time range
        year = dt.year
        start = self.__last_sunday_of_month(year, 3).replace(hour=1)
        end = self.__last_sunday_of_month(year, 10).replace(hour=1)

        if start <= dt.replace(tzinfo=None) < end:
            return timedelta(hours=1)
        else:
            return timedelta(hours=0)

    @staticmethod
    def __last_sunday_of_month(year, month):
        """
        Shows the last sunday of the month.

        Arguments:
            year (int) - A year.
            month (int) - A month.

        Returns:
            A day number.

        """
        # find last day of month
        last_sunday = datetime(year, month + 1, 1) - timedelta(days=1)
        # weekday(): monday = 0, ..., sunday = 6
        if last_sunday.weekday() < 6:  # last day in month isn't sunday
            day = last_sunday.day - (last_sunday.weekday() + 1)
            last_sunday = last_sunday.replace(day=day)
        return last_sunday
