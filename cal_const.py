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
#       2018-09-01  Robert Chapman
#                    - removed enums for standard cal repeating (rrule)
#
#########################################################################

import datetime

from enum import Enum, unique

#########################################################################
# Constants
#########################################################################

########################################
# Events
########################################
LOCATIONS = {1: 'Houge Park, Blg. 1',  # indoor
             2: 'Houge Park',          # outdoor
             3: 'Rancho Cañada del Oro',
             4: 'Mendoza Ranch',
             5: 'Coyote Valley',
             6: "Pinnacles Nat'l Park, East Side",
             7: "Pinnacles Nat'l Park, West Side",
             8: "Yosemite Nat'l Park, Glacier Point"}


########################################
# Rules that govern scheduling of events
########################################
@unique
class RuleLunar(Enum):
    """Lunar date rule, which phase of the moon do we want?"""
    moon_new = 0
    moon_1q = 1
    moon_full = 2
    moon_3q = 3

    def __str__(self):
        lut = ['New Moon', '1st Qtr Moon', 'Full Moon', '3rd Qtr Moon']
        return lut[self.value]


@unique
class RuleStartTime(Enum):
    """Solar time rule, which phase of sunset do we want for the time?"""
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
    '''Public/Private event?'''
    public = 'pu'
    member = 'me'
    private = 'pr'

    def __str__(self):
        lut = {'pu': 'public', 'me': 'member', 'pr': 'private'}
        return lut[self.value]
