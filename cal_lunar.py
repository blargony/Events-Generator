#########################################################################
#
#   Astronomy Club Lunar Ephemeris Data Generator
#   file: cal_lunar.py
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
#       2018-08-01  Robert Chapman, initial version
#
#########################################################################

import argparse
import csv
import datetime
import holidays

from dateutil import rrule

from cal_const import RuleStartTime, DAY
import cal_ephemeris

def holiday_weekend(date):
    hol = holidays.US()
    # Add the superbowl, first sunday in Feb.
    superb_owl = rrule.rrule(rrule.MONTHLY, count=1, byweekday=rrule.SU,
                             dtstart=datetime.date(date.year, 2, 1))
    hol.append({list(superb_owl)[0]: 'Superbowl Sunday'})

    if date.weekday() < 2:
        prev = 3 + date.weekday()   # 3 days prior minimum if Mon-Tues
        next = 2 - date.weekday()   # 1-2 days after for Mon-Tues
    elif date.weekday() > 2:
        prev = date.weekday() - 2   # 1 days prior for Thurs, more for later
        next = 8 - date.weekday()   # 1 day after for Sunday, more for earlier

    for i in range(-1 * prev, next):
        test_date = date + (i * DAY)
        holiday = hol.get(test_date)
        if holiday:
            return '{0} ({1})'.format(holiday, test_date.strftime('%b %-d'))


def gen_starttimes(rrule_gen):
    eph = cal_ephemeris.CalEphemeris()

    data = []
    data.append(['Date', 'Day', 'Sunset', 'Nautical Twilight',
                 'Illumination %', 'Moon Rise', 'Moon Set', 'Holiday'])
    for day in rrule_gen:
        entry = []
        entry.append(day.strftime('%b %-d %Y'))
        entry.append(day.strftime('%a'))
        entry.append(eph.get_sunset(day).strftime('%-I:%M %p'))
        entry.append(eph.get_sunset(day, RuleStartTime.nautical).strftime('%-I:%M %p'))
        try:
            entry.append(eph.moon_rise(day).strftime('%-I:%M %p'))
        except AttributeError:
            entry.append('')
        try:
            entry.append(eph.moon_set(day).strftime('%-I:%M %p'))
        except AttributeError:
            entry.append('')
        entry.append(round(eph.moon_illum(day)/100.0, 2))
        entry.append(holiday_weekend(day))
        data.append(entry)
    return data


def main():
    parser = argparse.ArgumentParser(description='Calendar Generator')
    parser.add_argument('--year', type=int, action='store', required=True,
                        help='Year of the generated Calendar')
    parser.add_argument('--filename', action='store',
                        help='Filename')
    args = parser.parse_args()


    start = datetime.datetime(args.year, 1, 1)
    until = datetime.datetime(args.year, 12, 31)
    rrule_gen = rrule.rrule(rrule.WEEKLY, dtstart=start, until=until,
                            byweekday=(rrule.FR, rrule.SA))
    data = gen_starttimes(rrule_gen)

    with open(args.filename, 'w') as fp:
        cfp = csv.writer(fp)
        for line in data:
            cfp.writerow(line)


# -------------------------------------
if __name__ == '__main__':
    exit(main())


