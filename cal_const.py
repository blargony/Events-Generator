#########################################################################
#
#   Astronomy Club Event Generator
#   file: cal_const.py
#
#   Copyright (C) 2016  Teruo Utsumi, San Jose Astronomical Association
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   Contributors:
#       2016-02-25  Teruo Utsumi, initial code
#       2018-07-31  Robert Chapman
#                    - moved ephemeris only consts to cal_ephemeris
#                    - moved LUTs into the enum classes
#
#########################################################################

import calendar
import datetime
import pytz
from enum import Enum, unique

#########################################################################
# Constants
#########################################################################
########################################
# Time/Time Format Strings
########################################
DAY = datetime.timedelta(days=1)
HOUR = datetime.timedelta(hours=1)
MINUTE = datetime.timedelta(minutes=1)
SECOND = datetime.timedelta(seconds=1)

TZ_UTC = pytz.timezone('UTC')
TZ_LOCAL = pytz.timezone('US/Pacific')

FMT_YEAR_DATE_HM = '%Y %a %m/%d %I:%M %p'
FMT_DATE_Y = '%a %m/%d %Y'
FMT_HM = '%I:%M %p'

########################################
# For Houge Park
########################################
LAT = '37.257465'
LONG = '-121.942281'
ELEVATION = 50

########################################
# Rules that govern scheduling of events
########################################
@unique
class RuleWeek(Enum):
    week_1 = 0
    week_2 = 1
    week_3 = 2
    week_4 = 3
    week_5 = 4

    def __str__(self):
        ordinal = ['st', 'nd', 'rd', 'th']
        week = self.value + 1
        return '{0}{1} week'.format(week, ordinal[week])


@unique
class RuleWeekday(Enum):
    monday = 'mo'
    tuesday = 'tu'
    wednesday = 'we'
    thursday = 'th'
    friday = 'fr'
    saturday = 'sa'
    sunday = 'su'

    def __int__(self):
        """Return standard datetime encoding, the week starts on Monday (0)."""
        lut = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}
        return lut[self.value]

    def __str__(self):
        return calendar.day_abbr[int(self)]


@unique
class RuleLunar(Enum):
    moon_new = 0
    moon_1q = 1
    moon_full = 2
    moon_3q = 3

    def __str__(self):
        lut = ['New Moon', '1st Qtr Moon', 'Full Moon', '3rd Qtr Moon']
        return lut[self.value]


@unique
class RuleStartTime(Enum):
    absolute = 'ab'  # start time specifies exact time
    sunset = 'su'  # others specfies period of day/twilight
    civil = 'ci'
    nautical = 'na'
    astronomical = 'as'

    def __str__(self):
        lut = {'ab': 'absolute', 'su': 'sunset', 'ci': 'civil',
               'na': 'nautical', 'as': 'astronomical'}
        return lut[self.value]

    @property
    def deg(self):
        lut = {'su': '0', 'ci': '-6', 'na': '-12', 'as': '-18'}
        return lut[self.value]


@unique
class EventVisibility(Enum):
    ephemeris = 'ep'
    public = 'pu'
    member = 'me'
    volunteer = 'vo'
    coordinator = 'co'
    private = 'pr'
    board = 'bo'
    observers = 'ob'
    imagers = 'im'

    def __str__(self):
        lut = {'ep': 'ephemeris', 'pu': 'public', 'me': 'member',
               'vo': 'volunteer', 'co': 'coordinator', 'pr': 'private',
               'bo': 'board', 'ob': 'observers', 'im': 'imagers'}
        return lut[self.value]


@unique
class EventRepeat(Enum):
    onetime = 'on'
    weekly = 'we'
    monthly = 'mo'
    lunar = 'lu'
    annual = 'an'

    def __str__(self):
        lut = {'on': 'one-time', 'we': 'weekly', 'mo': 'monthly',
               'lu': 'lunar', 'an': 'annual'}
        return lut[self.value]
