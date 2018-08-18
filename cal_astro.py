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
import icalendar

from dateutil import rrule

from cal_const import RuleStartTime, DAY
import cal_ephemeris


def get_holiday_cal(year):
    hol = holidays.US(years=year)
    # Add the superbowl, first Sunday in Feb.
    superb_owl = rrule.rrule(rrule.MONTHLY, count=1, byweekday=rrule.SU,
                             dtstart=datetime.date(year, 2, 1))
    hol.append({list(superb_owl)[0]: 'Superbowl Sunday'})
    # Mother's day, Second Sunday in May
    superb_owl = rrule.rrule(rrule.MONTHLY, count=1, byweekday=rrule.SU(2),
                             dtstart=datetime.date(year, 5, 1))
    hol.append({list(superb_owl)[0]: "Mother's Day"})
    # Father's day, Third Sunday in June
    superb_owl = rrule.rrule(rrule.MONTHLY, count=1, byweekday=rrule.SU(3),
                             dtstart=datetime.date(year, 6, 1))
    hol.append({list(superb_owl)[0]: "Father's Day"})

    return hol

def holiday_weekend(date):
    hol = get_holiday_cal(date.year)
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


def gen_lunar_data(rrule_gen):
    eph = cal_ephemeris.CalEphemeris()

    data = []
    for day in rrule_gen:
        entry = []
        entry.append(day)
        entry.append(day.strftime('%b %-d %Y'))
        entry.append(day.strftime('%a'))
        entry.append(eph.get_sunset(day).strftime('%-I:%M %p'))
        entry.append(eph.get_sunset(day, RuleStartTime.nautical).strftime('%-I:%M %p'))
        illum, rise, set = eph.get_moon_visibility(day)
        entry.append(int(round(illum)))
        try:
            if rise.strftime('%p') == 'AM':
                entry.append(rise.strftime('%-I:%M %p (%a)'))
            else:
                entry.append(rise.strftime('%-I:%M %p'))
        except AttributeError:
            entry.append('')
        try:
            if set.strftime('%p') == 'AM':
                entry.append(set.strftime('%-I:%M %p (%a)'))
            else:
                entry.append(set.strftime('%-I:%M %p'))
        except AttributeError:
            entry.append('')
        entry.append(holiday_weekend(day))
        data.append(entry)
    return data


def write_csv(filename, data):
    with open(filename, 'w') as fp:
        cfp = csv.writer(fp)
        header = ('Date', 'Day', 'Sunset', 'Nautical Twilight',
                  'Illumination %', 'Moon Rise', 'Moon Set', 'Holiday')
        cfp.writerow(header)
        for line in data:
            cfp.writerow(line[1:])    # omit the datetime object


def write_astro_ical(filename, data, year):
    cal = icalendar.Calendar()
    cal.add('prodid', 'Astro Calendar')
    cal.add('version', '2.0')
    for line in data:
        date = datetime.date(line[0].year, line[0].month, line[0].day)
        event = icalendar.Event()
        event.add('dtstart', date)
        event.add('summary', 'SS - {}, NT = {}\n'.format(line[3], line[4]))
        cal.add_component(event)

        event = icalendar.Event()
        event.add('dtstart', date)
        if line[5] < 10:
            event.add('summary', '{}% - New Moon'.format(line[5]))
        elif line[5] > 90:
            event.add('summary', '{}% - Full Moon'.format(line[5]))
        elif line[6]:
            event.add('summary', '{}% MR - {}'.format(line[5], line[6]))
        elif line[7]:
            event.add('summary', '{}% MS - {}'.format(line[5], line[7]))
        else:
            event.add('summary', '{}% Moon'.format(line[5]))
        cal.add_component(event)

    # Holidays
    hol = get_holiday_cal(year)
    for date, name in hol.items():
        event = icalendar.Event()
        event.add('dtstart', date)
        event.add('summary', '{}\n'.format(name))
        cal.add_component(event)

    eph = cal_ephemeris.CalEphemeris()
    dtstart = datetime.datetime(year, 1, 1)
    dtend = datetime.datetime(year, 12, 31)
    phases = list(eph.gen_moon_phases(dtstart, dtend))
    for phase, date in phases:
        event = icalendar.Event()
        event.add('dtstart', date.date())  # Cast to just date from datetime
        event.add('summary', '{}: {}\n'.format(phase, date.strftime('%-I:%M %p')))
        cal.add_component(event)

    with open(filename, 'wb') as fp:
        fp.write(cal.to_ical())


def main():
    parser = argparse.ArgumentParser(description='Calendar Generator')
    parser.add_argument('--year', type=int, action='store', required=True,
                        help='Year of the generated Calendar')
    parser.add_argument('--filename', action='store',
                        help='CSV Output Filename', default='astro.csv')
    parser.add_argument('--ifilename', action='store',
                        help='iCal Output Filename', default='astro.ics')
    args = parser.parse_args()


    start = datetime.datetime(args.year, 1, 1)
    until = datetime.datetime(args.year, 12, 31)
    # Get info for every Friday and Saturday
    rrule_gen = rrule.rrule(rrule.WEEKLY, dtstart=start, until=until,
                            byweekday=(rrule.FR, rrule.SA))
    data = gen_lunar_data(rrule_gen)
    write_csv(args.filename, data)
    write_astro_ical(args.ifilename, data, args.year)


# -------------------------------------
if __name__ == '__main__':
    exit(main())


