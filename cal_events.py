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

import datetime
import ephem
# import pdb
# import logging

from   cal_const     import *
import cal_ephemeris


# template for types of events, e.g., "In-town Star Party"
class EventType():
    type_id         = None
    name            = None
    visibility      = None
    tentative       = True
    coordinator_id  = None
    hide_location   = False
    location        = None
    repeat          = None  # lunar, monthly, ...
    lunar_phase     = None  # new, 1Q, full, 3Q
    day_of_week     = None  # Monday, ...
    rule_start_time = None  # absolute, sunset, civil, ..., rounded to 1/4 hour
    month           = None
    week            = None
    day_of_month    = None
    time_earliest   = None  # time
    time_start      = None  # time
    time_offset     = None  # timedelta
    time_length     = None  # timedelta
    email           = None
    url             = None
    notes           = None


class Event():
    event_id        = 0
    type_id         = 0
    name            = ''
    visibility      = 0
    tentative       = True
    deleted         = False
    canceled        = False
    sched_override  = False  # True if date/time changed manually
    coordinator_id  = 0
    hide_location   = False
    location        = 0
    rule_start_time = 0
    time_start      = 0
    time_length     = 0
    email           = None
    url             = ''
    notes           = ''
    date_created    = None
    date_updated    = None


def calc_monthly_dates(start, end, event_type):
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
        event_type  EventType

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

#   pdb.set_trace()
    date = start
    dates = []
    # set date to 1st of month
    date = date.replace(day=1)
#   pdb.set_trace()
    while date < end:
        weekday = weekday_to_int[event_type.day_of_week]
        week    = event_type.week.value
        # datetime.weekday - Monday=0, Sunday=6
        first_weekday_of_month = date.weekday()
        # calculate day of month
        if first_weekday_of_month > weekday:
            days = weekday - first_weekday_of_month + 7 + week*7
        else:
            days = weekday - first_weekday_of_month     + week*7
        # append date
        prev_month = date.month
        date = date + DAY*days
        new_month = date.month
        # reject date if additional days pushes date into next month
        if prev_month==new_month:
            # reject date before start and after end
            if start <= date <= end:
                date = TZ_LOCAL.localize(date.combine(date,
                                                      event_type.time_start))
                dates.append(date)
            # get month/year for following month
            next_month = date.month + 1
            next_year  = date.year
            if next_month > 12:
                next_month = 1
                next_year  += + 1
            try:
                date = date.replace(year=next_year, month=next_month, day=1)
            except:
                pdb.set_trace()
        else:
            date = date.replace(                  day=1)
    return dates


def calc_lunar_dates(start, end, event_type):
    '''
    Generate list of dates on a given weekday nearest the specified lunar
    phase in the period defined by (datetime) 'start' and 'end', inclusive.
    E.g.: 3Q Fridays @ nautical twilight

    input
        start       datetime.date   starting date of period to generate events
        end         datetime.date   ending   date of period to generate events
        event_type  EventType       default event template for type of event

    output
        return      list            tuples of datetime.datetime
    '''
    # set 'day' to 'weekday' at or after 'start'
    date = start
    dates = []
    weekday_of_date = date.weekday()
#   pdb.set_trace()
    event_weekday = weekday_to_int[event_type.day_of_week]
    if weekday_of_date > event_weekday:
        days = event_weekday - weekday_of_date + 7
    else:
        days = event_weekday - weekday_of_date
    date = date + DAY*days
    while date < end:
        dayofyear = int(date.strftime("%j"))
        if cal_ephemeris.moon_phase[dayofyear] == event_type.lunar_phase and \
           date <= end:
            if event_type.rule_start_time == RuleStartTime.absolute:
                time = event_type.time_start
                date = TZ_LOCAL.localize(date.combine(date, time))
            else:
                date = calc_start_time(date, event_type)
            if start < date:
                dates.append(date)
        date = date + DAY*7
    return dates


def calc_annual_dates(start, end, event_type):
    '''
    Generate list of dates on a given weekday nearest the specified lunar
    phase in the period defined by (datetime) 'start' and 'end', inclusive.
    E.g.: February full moon Saturday

    input
        start       datetime.date   starting date of period to generate events
        end         datetime.date   ending   date of period to generate events
        event_type  EventType       default event template for type of event

    output
        return      list            tuples of datetime.datetime
    '''
    # set 'date' to 'weekday' at or after 'start'
    date = start.replace(month=event_type.month, day=1)
    dates = []
    weekday_of_date = date.weekday()
#   pdb.set_trace()
    event_weekday = weekday_to_int[event_type.day_of_week]
    if weekday_of_date > event_weekday:
        days = event_weekday - weekday_of_date + 7
    else:
        days = event_weekday - weekday_of_date
    date = date + DAY*days
    while date < end:
        dayofyear = int(date.strftime("%j"))
        if cal_ephemeris.moon_phase[dayofyear] == event_type.lunar_phase and \
           date <= end:
            if event_type.rule_start_time == RuleStartTime.absolute:
                time = event_type.time_start
                date = TZ_LOCAL.localize(date.combine(date, time))
            else:
                date = calc_start_time(date, event_type)
            if start < date:
                dates.append(date)
                break
        date = date + DAY*7
    return dates


def calc_start_time(date, event_type):
    '''
    Calculate start time of event based on twilight time for 'date'.

    input
        date        datetime.date   date/time of event
        event_type  EventType       default event template for type of event

    output
        return      datetime        calculated start time
    '''

    if event_type.rule_start_time == RuleStartTime.absolute:
        date = TZ_LOCAL.localize(date.combine(date, event_type.time_start))
        return date
    local.date    = date.astimezone(TZ_UTC)
    try:
        local.horizon = rule_horizon[event_type.rule_start_time]
    except:
        pdb.set_trace()
    dusk = TZ_LOCAL.localize(ephem.localtime(local.next_setting(SUN)))
    old_h = dusk.hour
    old_m = dusk.minute
    new_h = old_h
    new_m = old_m
    # round minutes to nearest quarter hour
    if old_m <  5:
        new_m = 0
    elif old_m < 20:
        new_m = 15
    elif old_m < 35:
        new_m = 30
    elif old_m < 50:
        new_m = 45
    else:
        new_h += 1
        new_m  = 0
    date = date.replace(hour=new_h, minute=new_m) + event_type.time_offset
    # don't start before "earliest" (e.g., 7pm)
    if event_type.time_earliest and date.time() < event_type.time_earliest:
        # 'combine' doesn't keep timezone info
        date = TZ_LOCAL.localize(date.combine(date, event_type.time_earliest))
    return date
