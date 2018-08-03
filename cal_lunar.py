#########################################################################
#
#   Astronomy Club Event Generator
#   file: test.py
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

import argparse
import csv
import datetime
import holidays

from dateutil import rrule

from cal_const import RuleStartTime, RuleWeekday, DAY
import cal_ephemeris

def holiday_weekend(date):
    hol = holidays.US()

    if date.weekday() == int(RuleWeekday.friday):
        prev = 1
        next = 3
    elif date.weekday() == int(RuleWeekday.saturday):
        prev = 2
        next = 2

    for i in range(-1 * prev, next + 1):
        test_date = date - i * DAY
        holiday = hol.get(test_date)
        if holiday:
            return '{0} ({1})'.format(holiday, test_date.strftime('%b %-d'))


def gen_starttimes(rrule_gen):
    eph = cal_ephemeris.CalEphemeris()

    data = []
    data.append(['Date', 'Day', 'Sunset', 'Nautical Sunset', 'Moon Rise',
                 'Moon Set', 'Illumination %', 'Holiday'])
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


