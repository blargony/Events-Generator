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


# ==============================================================================
class CalEvent(object):
    '''Club Event date generator that follow the solar or lunar calendar.'''

    def __init__(self, eph, year):
        self.eph = eph   # cal_ephemeris object with the appropriate settings
        self.start = datetime(year, 1, 1)
        self.until = datetime(year, 12, 31)
        self.occurances = []

        # Event information
        self.name = None
        self.visibility = None
        self.location = None
        self.url = None
        self.description = None

        # Normal Calendar style
        self.date_rules = None   # rrule date generator

        # Lunar Calendar style
        self.lunar_rules = None    # new, 1Q, full, 3Q
        self.lunar_months = None   # Months to hold lunar events (None = all)

        # Specific Time
        self.start_time = None  # datetime.time object

        # Sunset Style Time
        self.sunset_type = None     # sunset, civil, nautical...
        self.time_earliest = None   # datetime.time
        self.time_offset = None     # datetime.timedelta from the sunset

        self.duration = None     # integer hours

    # --------------------------------------
    # Some helper functions to initialize properly
    # --------------------------------------
    def monthly(self, week, weekday):
        '''Monthly event, like in typical calendar fashion.'''
        self.date_rules = rrule.rrule(rrule.MONTHLY, byweekday=weekday(week),
                                      dtstart=self.start, until=self.until)

    def yearly(self, month, week, weekday):
        '''Monthly event, like in typical calendar fashion.'''
        self.date_rules = rrule.rrule(rrule.YEARLY,
                                      bymonth=month, byweekday=weekday(week),
                                      dtstart=self.start, until=self.until)

    def lunar(self, phase, weekday):
        '''Every lunar cycle, nearest the given phase.'''
        self.lunar_rules = phase
        self.date_rules = rrule.rrule(rrule.WEEKLY, byweekday=weekday,
                                      dtstart=self.start, until=self.until)

    def lunar_yearly(self, phase, weekday, months):
        '''Once a year near a lunar phase.'''
        self.lunar_rules = phase
        self.lunar_months = months
        self.date_rules = rrule.rrule(rrule.WEEKLY, byweekday=weekday,
                                      dtstart=self.start, until=self.until)

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
    def gen_occurances(self):
        if self.lunar_rules:
            return self.gen_lunar_dates()
        else:
            return self.gen_cal_dates()

    def gen_cal_dates(self):
        '''Generate all the occurances of the event'''
        for dt in self.date_rules:
            date = dt.date()
            dtstart, dtend = self.calc_times(date)
            self.occurances.append((dtstart, dtend))
        return self.occurances

    def gen_lunar_dates(self):
        '''Find the dates nearest the specified lunar phase'''
        days = list(self.date_rules)
        for phase, dt in self.eph.gen_moon_phases(start=self.start, until=self.until,
                                                  lunar_phase=self.lunar_rules):
            date = min(days, key=lambda x: abs(x - dt))
            dtstart, dtend = self.calc_times(date)
            self.occurances.append((dtstart, dtend))
        return self.occurances

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
        rounded_minute = round(dusk.minute/15.0) * 15
        if rounded_minute == 60:
            rounded_hour += 1
            rounded_minute = 0
        date = date.replace(hour=rounded_hour, minute=rounded_minute) + self.time_offset

        # don't start before "earliest" (e.g., 7pm)
        if self.time_earliest and date.time() < self.time_earliest:
            date = date.combine(date, self.time_earliest)
        return date, date + self.duration

    # --------------------------------------
    def as_ical_events(self, cal):
        '''Add all generated events to the given calendar object.'''
        for dtstart, dtend in self.occurances:
            event = icalendar.Event()
            if dtend:
                event.add('dtstart', dtstart)
                event.add('dtend', dtend)
            else:
                event.add('dtstart', dtstart.date())
            event.add('summary', self.name)
            cal.add_component(event)


