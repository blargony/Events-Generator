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
#
#########################################################################

import calendar
import datetime
import pytz
import ephem
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
# Ephem Constants
########################################
SUN = ephem.Sun()
MOON = ephem.Moon()
PLANETS = (ephem.Mars(), ephem.Jupiter(), ephem.Saturn(),
           ephem.Uranus(), ephem.Neptune(), ephem.Pluto())

SEASONS = {
    'spring': (ephem.next_vernal_equinox, 'Spring Equinox'),
    'summer': (ephem.next_summer_solstice, 'Summer Solstice'),
    'fall': (ephem.next_autumn_equinox, 'Fall Equinox'),
    'winter': (ephem.next_winter_solstice, 'Winter Solstice')
}

EPHEM_SECOND = ephem.second
EPHEM_DAY = ephem.hour*24
EPHEM_MONTH = EPHEM_DAY*30

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
class RuleLunar(Enum):
    moon_new = 0
    moon_1q = 1
    moon_full = 2
    moon_3q = 3


@unique
class RuleStartTime(Enum):
    absolute = 'ab'  # start time specifies exact time
    sunset = 'su'  # others specfies period of day/twilight
    civil = 'ci'
    nautical = 'na'
    astronomical = 'as'


@unique
class RuleWeekday(Enum):
    monday = 'mo'
    tuesday = 'tu'
    wednesday = 'we'
    thursday = 'th'
    friday = 'fr'
    saturday = 'sa'
    sunday = 'su'


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


@unique
class EventRepeat(Enum):
    onetime = 'on'
#   weekly       = 'we'  # not currently supported
    monthly = 'mo'
    lunar = 'lu'
    annual = 'an'


########################################
# display strings corresponding to above rules
########################################
rule_week = {RuleWeek.week_1: '1st week',
             RuleWeek.week_2: '2nd week',
             RuleWeek.week_3: '3rd week',
             RuleWeek.week_4: '4th week',
             RuleWeek.week_5: '5th week'}

rule_weekday = {RuleWeekday.sunday: calendar.day_abbr[6],
                RuleWeekday.monday: calendar.day_abbr[0],
                RuleWeekday.tuesday: calendar.day_abbr[1],
                RuleWeekday.wednesday: calendar.day_abbr[2],
                RuleWeekday.thursday: calendar.day_abbr[3],
                RuleWeekday.friday: calendar.day_abbr[4],
                RuleWeekday.saturday: calendar.day_abbr[5]}

# to match datetime.weekday()
weekday_to_int = {RuleWeekday.sunday: 6,
                  RuleWeekday.monday: 0,
                  RuleWeekday.tuesday: 1,
                  RuleWeekday.wednesday: 2,
                  RuleWeekday.thursday: 3,
                  RuleWeekday.friday: 4,
                  RuleWeekday.saturday: 5}

##########################
# for astronomy scheduling
##########################
rule_start_time = {RuleStartTime.absolute: 'absolute',
                   RuleStartTime.sunset: 'sunset',
                   RuleStartTime.civil: 'civil',
                   RuleStartTime.nautical: 'nautical',
                   RuleStartTime.astronomical: 'astronomical'}

rule_lunar = {RuleLunar.moon_new: 'new moon',
              RuleLunar.moon_1q: '1Q moon',
              RuleLunar.moon_full: 'full moon',
              RuleLunar.moon_3q: '3Q moon'}

rule_horizon = {RuleStartTime.sunset: '0',
                RuleStartTime.civil: '-6',
                RuleStartTime.nautical: '-12',
                RuleStartTime.astronomical: '-18'}

##########################
event_visibility = {EventVisibility.ephemeris: 'ephemeris',
                    EventVisibility.public: 'public',
                    EventVisibility.member: 'member',
                    EventVisibility.volunteer: 'volunteer',
                    EventVisibility.coordinator: 'coordinator',
                    EventVisibility.private: 'private',
                    EventVisibility.board: 'board'}

event_repeat = {EventRepeat.onetime: 'one-time',
                EventRepeat.monthly: 'monthly',
                #                    EventRepeat.weekly          : 'weekly'      ,
                EventRepeat.lunar: 'lunar',
                EventRepeat.annual: 'annual'}

