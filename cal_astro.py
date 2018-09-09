'''
  Astronomy Club Lunar Ephemeris Data Generator
  file: cal_lunar.py

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
      2018-08-01  Robert Chapman, initial version
'''

import argparse
import csv
import datetime
import icalendar

from dateutil import rrule

import cal_ephemeris
import cal_holidays


def gen_lunar_data(rrule_gen, eph, hol):
    '''Return a list of lunar events for every date from the rrule.'''
    data = []
    for day in rrule_gen:
        entry = []
        entry.append(day)
        entry.append(day.strftime('%b %-d %Y'))
        entry.append(day.strftime('%a'))
        entry.append(eph.get_sunset(day).strftime('%-I:%M %p'))
        entry.append(
            eph.get_sunset(
                day, cal_ephemeris.RuleSunset.nautical).strftime('%-I:%M %p'))
        illum, moon_rise, moon_set = eph.get_moon_visibility(day)
        entry.append(int(round(illum)))
        try:
            if moon_rise.strftime('%p') == 'AM':
                entry.append(moon_rise.strftime('%-I:%M %p (%a)'))
            else:
                entry.append(moon_rise.strftime('%-I:%M %p'))
        except AttributeError:
            entry.append('')
        try:
            if moon_set.strftime('%p') == 'AM':
                entry.append(moon_set.strftime('%-I:%M %p (%a)'))
            else:
                entry.append(moon_set.strftime('%-I:%M %p'))
        except AttributeError:
            entry.append('')
        entry.append(hol.holiday_weekend(day))
        data.append(entry)
    return data


def write_csv(filename, data):
    '''Write out a list of lists into a CSV file.'''
    with open(filename, 'w') as cfp:
        cfp = csv.writer(cfp)
        header = ('Date', 'Day', 'Sunset', 'Nautical Twilight',
                  'Illumination %', 'Moon Rise', 'Moon Set', 'Holiday')
        cfp.writerow(header)
        for line in data:
            cfp.writerow(line[1:])  # omit the datetime object


def write_astro_ical(filename, start, until, data, eph, hol):
    '''Write out lunar data and other events in an iCal compatible format.'''
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
    for date, name in hol.get_holidays():
        event = icalendar.Event()
        event.add('dtstart', date)
        event.add('summary', '{}\n'.format(name))
        cal.add_component(event)

    # Moon Phases
    for phase, date in eph.gen_moon_phases(start, until):
        event = icalendar.Event()
        event.add('dtstart', date.date())  # Cast to just date from datetime
        event.add('summary', '{}: {}\n'.format(
            str(phase), date.strftime('%-I:%M %p')))
        cal.add_component(event)

    with open(filename, 'wb') as icfp:
        icfp.write(cal.to_ical())


def main():
    '''Main, silly lint tool.'''
    parser = argparse.ArgumentParser(description='Calendar Generator')
    parser.add_argument(
        '--year',
        type=int,
        action='store',
        required=True,
        help='Year of the generated Calendar')
    parser.add_argument(
        '--filename',
        action='store',
        help='CSV Output Filename',
        default='astro.csv')
    parser.add_argument(
        '--ifilename',
        action='store',
        help='iCal Output Filename',
        default='astro.ics')
    args = parser.parse_args()

    eph = cal_ephemeris.CalEphemeris()
    hol = cal_holidays.CalHoliday(args.year)

    # Get info for every Friday and Saturday
    start = datetime.datetime(args.year, 1, 1)
    until = datetime.datetime(args.year, 12, 31)
    rrule_gen = rrule.rrule(
        rrule.WEEKLY,
        dtstart=start,
        until=until,
        byweekday=(rrule.FR, rrule.SA))

    data = gen_lunar_data(rrule_gen, eph, hol)
    write_csv(args.filename, data)
    write_astro_ical(args.ifilename, start, until, data, eph, hol)


# -------------------------------------
if __name__ == '__main__':
    exit(main())
