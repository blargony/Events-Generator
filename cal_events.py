'''

  Astronomy Club Event Generator
  file: cal_events.py

  Copyright (C) 2016  Teruo Utsumi, San Jose Astronomical Association

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  Contributors:
      2016-02-25  Teruo Utsumi, initial code
      2018-07-21  Robert Chapman, streamlined to single CalEvent class
      2018-08-15  Robert Chapman, line cleanup
      2018-09-01  Robert Chapman, refactor to incorporate dateutil.rrule
'''
from datetime import datetime, timedelta
import icalendar

from dateutil import rrule
from enum import Enum, unique

# ==============================================================================
# Constants
# ==============================================================================
MON = rrule.MO
TUE = rrule.TU
WED = rrule.WE
THU = rrule.TH
FRI = rrule.FR
SAT = rrule.SA
SUN = rrule.SU

LOCATIONS = {
    1: 'Houge Park, Blg. 1',  # indoor
    2: 'Houge Park',  # outdoor
    3: 'Rancho Cañada del Oro',
    4: 'Mendoza Ranch',
    5: 'Coyote Valley',
    6: "Pinnacles Nat'l Park, East Side",
    7: "Pinnacles Nat'l Park, West Side",
    8: "Yosemite Nat'l Park, Glacier Point"
}


# ==============================================================================
# Enumerated Types for scheduling of events
# ==============================================================================
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
class RuleSunset(Enum):
    """Solar time rule, which phase of sunset do we want for the time?"""
    sunset = 'su'  # others specfies period of day/twilight
    civil = 'ci'
    nautical = 'na'
    astronomical = 'as'

    def __str__(self):
        lut = {
            'su': 'sunset',
            'ci': 'civil',
            'na': 'nautical',
            'as': 'astronomical'
        }
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


# ==============================================================================
class CalEvent(object):
    '''Club Event date generator that follow the solar or lunar calendar.'''

    def __init__(self, eph):
        self.eph = eph  # cal_ephemeris object with the appropriate settings

        # Event information
        self.name = None
        self.visibility = None
        self.location = None
        self.url = None
        self.description = None

        # Normal Calendar style
        self.date_rules = None  # rrule date generator

        # Lunar Calendar style
        self.lunar_rules = None  # new, 1Q, full, 3Q
        self.lunar_months = None  # Months to hold lunar events (None = all)

        # Specific Time
        self.start_time = None  # datetime.time object

        # Sunset Style Time
        self.sunset_type = None  # sunset, civil, nautical...
        self.time_earliest = None  # datetime.time
        self.time_offset = None  # datetime.timedelta from the sunset

        self.duration = None  # integer hours

    # --------------------------------------
    # Some helper functions to initialize properly
    # --------------------------------------
    def monthly(self, week, weekday):
        '''Monthly event, like in typical calendar fashion.'''
        self.date_rules = rrule.rrule(
            rrule.MONTHLY, byweekday=weekday(week),
            count=1000)  # generously large but not infinite event count

    def yearly(self, month, week, weekday):
        '''Monthly event, like in typical calendar fashion.'''
        self.date_rules = rrule.rrule(
            rrule.YEARLY, bymonth=month, byweekday=weekday(week), count=1000)

    def lunar(self, phase, weekday):
        '''On given weekday every lunar cycle, nearest the given phase.'''
        self.lunar_rules = phase
        self.date_rules = rrule.rrule(
            rrule.WEEKLY, byweekday=weekday, count=1000)

    def lunar_yearly(self, phase, weekday, months):
        '''Yearly near a lunar phase, on the given weekday/months.'''
        self.lunar_rules = phase
        self.lunar_months = months
        self.date_rules = rrule.rrule(
            rrule.YEARLY, bymonth=months, byweekday=weekday, count=1000)

    def times(self, start_time, duration=1):
        '''Once a year near a lunar phase.'''
        self.start_time = start_time
        self.duration = timedelta(hours=duration)

    def sunset_times(self, sunset_type, earliest, offset=0, length=1):
        '''Once a year near a lunar phase.'''
        self.sunset_type = sunset_type

        self.time_earliest = earliest
        self.time_offset = timedelta(hours=offset)
        self.duration = timedelta(hours=length)

    # --------------------------------------
    def gen_occurances(self, start, until):
        if self.lunar_rules:
            return self.gen_lunar_dates(start, until)
        else:
            return self.gen_cal_dates(start, until)

    def gen_dates(self, start, until):
        days = list(self.date_rules)
        return [d for d in days if d > start and d < until]

    def gen_cal_dates(self, start, until):
        '''Generate all the occurances of the event'''
        occurances = []
        for dt in self.gen_dates(start, until):
            dt = dt.date()
            dtstart, dtend = self.calc_times(dt)
            occurances.append((dtstart, dtend))
        return occurances

    def gen_lunar_dates(self, start, until):
        '''Find the dates nearest the specified lunar phase'''
        occurances = []
        days = self.gen_dates(start, until)
        for phase, dt in self.eph.gen_moon_phases(
                start, until, lunar_phase=self.lunar_rules):
            if not self.lunar_months or dt.month in self.lunar_months:
                dt = min(days, key=lambda x: abs(x - dt))
                dtstart, dtend = self.calc_times(dt)
                occurances.append((dtstart, dtend))
        return occurances

    # --------------------------------------
    def calc_times(self, date):
        if self.start_time:
            start = datetime.combine(date, self.start_time)
            return start, start + self.duration
        else:
            return self.calc_sunset_times(date)

    def calc_sunset_times(self, date):
        '''Calculate start time of event based on twilight time for 'date'.'''
        dusk = self.eph.get_sunset(date, self.sunset_type)

        # round minutes to nearest quarter hour
        rounded_hour = dusk.hour
        rounded_minute = round(dusk.minute / 15.0) * 15
        if rounded_minute == 60:
            rounded_hour += 1
            rounded_minute = 0
        date = date.replace(
            hour=rounded_hour, minute=rounded_minute) + self.time_offset

        # don't start before "earliest" (e.g., 7pm)
        if self.time_earliest and date.time() < self.time_earliest:
            date = date.combine(date, self.time_earliest)
        return date, date + self.duration

    # --------------------------------------
    def add_ical_events(self, start, until, cal):
        '''Add all generated events to the given calendar object.'''
        for dtstart, dtend in self.gen_occurances(start, until):
            event = icalendar.Event()
            if dtend:
                event.add('dtstart', dtstart)
                event.add('dtend', dtend)
            else:
                event.add('dtstart', dtstart.date())
            event.add('summary', self.name)
            cal.add_component(event)
