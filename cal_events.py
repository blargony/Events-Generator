#########################################################################
#
#   Astronomy Club Event Generator
#   file: cal_events.py
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

import cal_ephemeris
from cal_const import *

# template for types of events, e.g., "In-town Star Party"
class CalEvent():
    name = None
    visibility = None
    location = None
    repeat = None  # lunar, monthly, ...
    lunar_phase = None  # new, 1Q, full, 3Q
    day_of_week = None  # Monday, ...
    rule_start_time = None  # absolute, sunset, civil, ..., rounded to 1/4 hour
    month = None
    week = None
    day_of_month = None
    time_earliest = None  # time
    time_start = None  # time
    time_offset = None  # timedelta
    time_length = None  # timedelta
    email = None
    url = None
    notes = None

    def get_ephem(self):
        return cal_ephemeris.CalEphemeris()

    def calc_monthly_dates(self, start, end):
        '''
        Generate list of datetime for monthly events on nth weekday given week
        and day of the week of each month.
        E.g., to calculate 2nd Tuesday of March, 1999:
            calc_monthly_dates(<start datetime>, <end datetime>, RuleWeek.week_2,
                            RuleWeekday.tuesday.value())
            (Note: the date must be between start and end datetimes

        Look for all dates in complete months.  Then throw away dates not
        between start and end, inclusive.

        Be sure time for 'start' and 'end' are '0:00'.
        'week': Zero means 1st week.

        input
            start       datetime.date   starting date of period to generate events
            end         datetime.date   ending   date of period to generate events

        output
            return list of datetime.datetime of scheduled events

        test:
            use above 'def a'
            input:
                start = datetime.datetime(2016, 2, 1)
                end   = datetime.datetime(2016, 9, 30)
                a(start, end, RuleWeek.week_5, RuleWeekday.tuesday) # 5th Tuesday
            output:
                2016-03-29 00:00:00
                2016-05-31 00:00:00
                2016-08-30 00:00:00
        '''

        dates = []
        date = start
        weekday = weekday_to_int[self.day_of_week]
        week = self.week.value

        while date < end:
            # set date to 1st of month
            date = date.replace(day=1)
            # datetime.weekday - Monday=0, Sunday=6
            first_weekday_of_month = date.weekday()

            # calculate day of month
            if first_weekday_of_month > weekday:
                days = weekday - first_weekday_of_month + 7 + week * 7
            else:
                days = weekday - first_weekday_of_month + week * 7
            prev_month = date.month
            date = date + DAY * days
            new_month = date.month

            # reject date if additional days pushes date into next month
            if prev_month == new_month:
                # reject date before start and after end
                if start <= date <= end:
                    date = TZ_LOCAL.localize(date.combine(date, self.time_start))
                    dates.append(date)

            # Increment the month
            date = date.replace(day=1)
            date = date + DAY * 32   # Definitely will hit the next month
        return dates


    def calc_lunar_dates(self, start, end):
        """Generate list of dates on a given weekday nearest the specified lunar
        phase in the period defined by (datetime) 'start' and 'end', inclusive.

        E.g.: 3Q Fridays @ nautical twilight

        input
            start       datetime.date   starting date of period to generate events
            end         datetime.date   ending   date of period to generate events

        output
            return      list            tuples of datetime.datetime
        """
        cal_eph = self.get_ephem()
        cal_eph.gen_astro_data(start.year)

        # set 'day' to 'weekday' at or after 'start'
        date = start
        dates = []
        weekday = weekday_to_int[self.day_of_week]
        weekday_of_date = date.weekday()

        if weekday_of_date > weekday:
            days = weekday - weekday_of_date + 7
        else:
            days = weekday - weekday_of_date
        date = date + DAY * days

        while date < end:
            dayofyear = int(date.strftime('%j'))
            if cal_eph.moon_phase[dayofyear] == self.lunar_phase and date <= end:
                if self.rule_start_time == RuleStartTime.absolute:
                    time = self.time_start
                    date = TZ_LOCAL.localize(date.combine(date, time))
                else:
                    date = self.calc_start_time(date)
                if start < date:
                    dates.append(date)
            date = date + DAY*7
        return dates


    def calc_annual_dates(self, start, end):
        '''
        Generate list of dates on a given weekday nearest the specified lunar
        phase in the period defined by (datetime) 'start' and 'end', inclusive.
        E.g.: February full moon Saturday

        input
            start       datetime.date   starting date of period to generate events
            end         datetime.date   ending   date of period to generate events

        output
            return      list            tuples of datetime.datetime
        '''
        cal_eph = self.get_ephem()
        cal_eph.gen_astro_data(start.year)

        # set 'date' to 'weekday' at or after 'start'
        date = start.replace(month=self.month, day=1)
        dates = []
        weekday_of_date = date.weekday()
        event_weekday = weekday_to_int[self.day_of_week]
        if weekday_of_date > event_weekday:
            days = event_weekday - weekday_of_date + 7
        else:
            days = event_weekday - weekday_of_date
        date = date + DAY*days

        while date < end:
            dayofyear = int(date.strftime('%j'))
            if cal_eph.moon_phase[dayofyear] == self.lunar_phase and date <= end:
                if self.rule_start_time == RuleStartTime.absolute:
                    time = self.time_start
                    date = TZ_LOCAL.localize(date.combine(date, time))
                else:
                    date = self.calc_start_time(date)
                if start < date:
                    dates.append(date)
                    break
            date = date + DAY*7
        return dates


    def calc_start_time(self, date):
        """Calculate start time of event based on twilight time for 'date'.

        input
            date        datetime.date   date/time of event

        output
            return      datetime        calculated start time
        """

        if self.rule_start_time == RuleStartTime.absolute:
            date = TZ_LOCAL.localize(date.combine(date, self.time_start))
            return date

        cal_eph = self.get_ephem()
        cal_eph.observer.date = date.astimezone(TZ_UTC)
        cal_eph.observer.horizon = rule_horizon[self.rule_start_time]
        dusk = cal_eph.get_sunset()

        # round minutes to nearest quarter hour
        rounded_hour = dusk.hour
        rounded_minute = round(dusk.minute/15.0) * 15
        if rounded_minute == 60:
            rounded_hour += 1
            rounded_minute = 0
        date = date.replace(hour=rounded_hour, minute=rounded_minute) + self.time_offset

        # don't start before "earliest" (e.g., 7pm)
        if self.time_earliest and date.time() < self.time_earliest:
            # 'combine' doesn't keep timezone info
            date = TZ_LOCAL.localize(date.combine(date, self.time_earliest))
        return date
