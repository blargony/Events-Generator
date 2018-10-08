#########################################################################
#
#   Astronomy Club Event Generator
#   file: cal_gen.py
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
#       2018-09-02  Robert Chapman
#                     - Updated for modified cal_events
#                     - Changed output format to CSV and iCal
#
#########################################################################

import argparse
import csv
import datetime
import icalendar

import cal_events
import cal_ephemeris


# ==============================================================================
# Generate a calendar of events
# ==============================================================================
class CalGen():
    """Wrap the list of SJAA Events for the year."""
    def __init__(self):
        self.eph = cal_ephemeris.CalEphemeris()
        self.events = []
        self.init_events()

    def init_events(self):
        """Put all event objects here, with the date/time rules."""
        class_intro = cal_events.CalEvent(self.eph)
        class_intro.name = 'Intro to the Night Sky'
        class_intro.visibility = cal_events.EventVisibility.public
        class_intro.location = cal_events.LOCATIONS[1]
        class_intro.url = 'www.sjaa.net/programs/beginners-astronomy'
        class_intro.description = ''
        class_intro.lunar(cal_events.RuleLunar.moon_1q, cal_events.FRI)
        class_intro.sunset_times(cal_events.RuleSunset.nautical,
                                 datetime.time(hour=19), -1, 1)
        self.events.append(class_intro)

        class_101 = cal_events.CalEvent(self.eph)
        class_101.name = 'Astronomy 101'
        class_101.visibility = cal_events.EventVisibility.public
        class_101.location = cal_events.LOCATIONS[1]
        class_101.url = 'www.sjaa.net/programs/beginners-astronomy'
        class_101.description = ''
        class_101.lunar(cal_events.RuleLunar.moon_3q, cal_events.FRI)
        class_101.sunset_times(cal_events.RuleSunset.nautical,
                               datetime.time(hour=19), -1, 1)
        self.events.append(class_101)

        itsp_1q = cal_events.CalEvent(self.eph)
        itsp_1q.name = 'In-town Star Party'
        itsp_1q.visibility = cal_events.EventVisibility.public
        itsp_1q.location = cal_events.LOCATIONS[2]
        itsp_1q.url = 'www.sjaa.net/events/monthly-star-parties'
        itsp_1q.description = '1st quarter moon ITSP'
        itsp_1q.lunar(cal_events.RuleLunar.moon_1q, cal_events.FRI)
        itsp_1q.sunset_times(cal_events.RuleSunset.nautical,
                             datetime.time(hour=19), 0, 3)
        self.events.append(itsp_1q)

        itsp_3q = cal_events.CalEvent(self.eph)
        itsp_3q.name = 'In-town Star Party'
        itsp_3q.visibility = cal_events.EventVisibility.public
        itsp_3q.location = cal_events.LOCATIONS[2]
        itsp_3q.url = 'www.sjaa.net/events/monthly-star-parties'
        itsp_3q.description = '3rd quarter moon ITSP'
        itsp_3q.lunar(cal_events.RuleLunar.moon_3q, cal_events.FRI)
        itsp_3q.sunset_times(cal_events.RuleSunset.nautical,
                             datetime.time(hour=19), 0, 3)
        self.events.append(itsp_3q)

        starry_night = cal_events.CalEvent(self.eph)
        starry_night.name = 'Starry Night (OSA)'
        starry_night.visibility = cal_events.EventVisibility.public
        starry_night.location = cal_events.LOCATIONS[3]
        starry_night.url = 'www.sjaa.net/events/starry-nights-public-star-party/'
        starry_night.description = 'Starry Nights hosted by the Open Space Authority'
        starry_night.lunar_yearly(
            cal_events.RuleLunar.moon_3q,
            cal_events.SAT,
            months=(2, 3, 4, 5, 6, 7, 8, 9, 10))
        starry_night.sunset_times(cal_events.RuleSunset.civil, None, 0, 3)
        self.events.append(starry_night)

        dark_sky = cal_events.CalEvent(self.eph)
        dark_sky.name = 'Dark Sky Night'
        dark_sky.visibility = cal_events.EventVisibility.member
        dark_sky.location = cal_events.LOCATIONS[4]
        dark_sky.url = 'www.sjaa.net/dark-sky-nights??'
        dark_sky.description = ''
        dark_sky.lunar(cal_events.RuleLunar.moon_new, cal_events.SAT)
        dark_sky.sunset_times(cal_events.RuleSunset.civil,
                              datetime.time(hour=19), 0, 4)
        self.events.append(dark_sky)

        quick_start = cal_events.CalEvent(self.eph)
        quick_start.name = 'Quick STARt'
        quick_start.visibility = cal_events.EventVisibility.private
        quick_start.location = cal_events.LOCATIONS[1]
        quick_start.url = 'www.sjaa.net/programs/quick-start'
        quick_start.description = ''
        quick_start.lunar(cal_events.RuleLunar.moon_1q, cal_events.SAT)
        quick_start.times(datetime.time(hour=19), 2)
        self.events.append(quick_start)

        solar_sunday = cal_events.CalEvent(self.eph)
        solar_sunday.name = 'Solar Sunday'
        solar_sunday.visibility = cal_events.EventVisibility.public
        solar_sunday.location = cal_events.LOCATIONS[1]
        solar_sunday.url = 'www.sjaa.net/solar-observing??'
        solar_sunday.description = ''
        solar_sunday.monthly(1, cal_events.SUN)
        solar_sunday.times(datetime.time(hour=13), 2)
        self.events.append(solar_sunday)

        img_workshop = cal_events.CalEvent(self.eph)
        img_workshop.name = 'Imaging Workshop'
        img_workshop.visibility = cal_events.EventVisibility.public
        img_workshop.location = cal_events.LOCATIONS[5]
        img_workshop.url = 'https://www.sjaa.net/programs/imaging-sig/'
        img_workshop.description = ''
        img_workshop.lunar_yearly(
            cal_events.RuleLunar.moon_new,
            cal_events.SAT,
            months=(1, 2, 4, 5, 7, 8, 9, 10))
        img_workshop.sunset_times(cal_events.RuleSunset.nautical,
                                  datetime.time(hour=19), 0, 3)
        self.events.append(img_workshop)

        img_clinic = cal_events.CalEvent(self.eph)
        img_clinic.name = 'Imaging Clinic'
        img_clinic.visibility = cal_events.EventVisibility.public
        img_clinic.location = cal_events.LOCATIONS[5]
        img_clinic.url = 'https://www.sjaa.net/programs/imaging-sig/'
        img_clinic.description = ''
        img_clinic.lunar_yearly(
            cal_events.RuleLunar.moon_new,
            cal_events.SAT,
            months=(3, 6, 9, 12))
        img_clinic.sunset_times(cal_events.RuleSunset.nautical,
                                datetime.time(hour=19), 0, 3)
        self.events.append(img_clinic)

        bino = cal_events.CalEvent(self.eph)
        bino.name = 'Binocular Observing'
        bino.visibility = cal_events.EventVisibility.public
        bino.location = cal_events.LOCATIONS[5]
        bino.url = 'https://www.sjaa.net/events/binocular-stargazing/'
        bino.description = ''
        bino.lunar_yearly(
            cal_events.RuleLunar.moon_3q,
            cal_events.SAT,
            months=(5, 6, 7, 8))
        bino.sunset_times(cal_events.RuleSunset.nautical,
                          datetime.time(hour=19), 0, 3)
        self.events.append(bino)

        pinnacles = cal_events.CalEvent(self.eph)
        pinnacles.name = 'Pinnacles Dark Sky Observing (NPS)'
        pinnacles.visibility = cal_events.EventVisibility.public
        pinnacles.location = cal_events.LOCATIONS[6]
        pinnacles.url = 'https://www.sjaa.net/events/pinnacles-stargazing/'
        pinnacles.description = ''
        pinnacles.lunar_yearly(
            cal_events.RuleLunar.moon_new,
            cal_events.SAT,
            months=(5, 6, 7, 8))
        pinnacles.sunset_times(cal_events.RuleSunset.nautical,
                               datetime.time(hour=19), 0, 3)
        self.events.append(pinnacles)

        fix_it = cal_events.CalEvent(self.eph)
        fix_it.name = 'Fix It'
        fix_it.visibility = cal_events.EventVisibility.public
        fix_it.location = cal_events.LOCATIONS[2]
        fix_it.url = 'www.sjaa.net/programs/fix-it'
        fix_it.description = ''
        fix_it.monthly(1, cal_events.SUN)
        fix_it.times(datetime.time(hour=14), 2)
        self.events.append(fix_it)

        image_sig = cal_events.CalEvent(self.eph)
        image_sig.name = 'Imaging SIG'
        image_sig.visibility = cal_events.EventVisibility.public
        image_sig.location = cal_events.LOCATIONS[1]
        image_sig.url = 'www.sjaa.net/programs/imaging-sig'
        image_sig.description = ''
        image_sig.monthly(3, cal_events.TUE)
        image_sig.times(datetime.time(hour=19, minute=30), 2)
        self.events.append(image_sig)

        board_mtg = cal_events.CalEvent(self.eph)
        board_mtg.name = 'Board Meeting'
        board_mtg.visibility = cal_events.EventVisibility.member
        board_mtg.location = cal_events.LOCATIONS[1]
        board_mtg.url = 'www.sjaa.net/board-meeting??'
        board_mtg.description = ''
        board_mtg.lunar(cal_events.RuleLunar.moon_full, cal_events.SAT)
        board_mtg.times(datetime.time(hour=18), 2)
        self.events.append(board_mtg)

        gen_mtg = cal_events.CalEvent(self.eph)
        gen_mtg.name = 'General Meeting'
        gen_mtg.visibility = cal_events.EventVisibility.public
        gen_mtg.location = cal_events.LOCATIONS[1]
        gen_mtg.url = 'www.sjaa.net/programs/monthly-guest-speakers'
        gen_mtg.description = ''
        gen_mtg.lunar_yearly(
            cal_events.RuleLunar.moon_full,
            cal_events.SAT,
            months=(1, 3, 4, 5, 6, 7, 10, 11, 12))  # Skip special meetings
        gen_mtg.times(datetime.time(hour=19, minute=30), 2)
        self.events.append(gen_mtg)

        mem_mtg = cal_events.CalEvent(self.eph)
        mem_mtg.name = 'Membership Meeting/Awards Night'
        mem_mtg.visibility = cal_events.EventVisibility.member
        mem_mtg.location = cal_events.LOCATIONS[1]
        mem_mtg.url = 'www.sjaa.net/membership-meeting??'
        mem_mtg.description = ''
        mem_mtg.lunar_yearly(
            cal_events.RuleLunar.moon_full, cal_events.SAT, months=(2, ))
        mem_mtg.times(datetime.time(hour=19, minute=30), 2)
        self.events.append(mem_mtg)

        movie_night = cal_events.CalEvent(self.eph)
        movie_night.name = 'Movie Night'
        movie_night.visibility = cal_events.EventVisibility.member
        movie_night.location = cal_events.LOCATIONS[1]
        movie_night.url = 'www.sjaa.net/movie-night'
        movie_night.description = 'Member Only Movie Night'
        movie_night.lunar_yearly(
            cal_events.RuleLunar.moon_full, cal_events.SAT, months=(8, ))
        movie_night.times(datetime.time(hour=19, minute=30), 2)
        self.events.append(movie_night)

        show_n_tell = cal_events.CalEvent(self.eph)
        show_n_tell.name = 'Show-n-tell'
        show_n_tell.visibility = cal_events.EventVisibility.public
        show_n_tell.location = cal_events.LOCATIONS[1]
        show_n_tell.url = 'www.sjaa.net/events/show-n-tell??'
        show_n_tell.description = ''
        show_n_tell.lunar_yearly(
            cal_events.RuleLunar.moon_full, cal_events.SAT, months=(9, ))
        show_n_tell.times(datetime.time(hour=19, minute=30), 2)
        self.events.append(show_n_tell)

        swap_spring = cal_events.CalEvent(self.eph)
        swap_spring.name = 'Spring Swap Meet'
        swap_spring.visibility = cal_events.EventVisibility.public
        swap_spring.location = cal_events.LOCATIONS[1]
        swap_spring.url = 'www.sjaa.net/events/swap-meet'
        swap_spring.description = ''
        swap_spring.lunar_yearly(
            cal_events.RuleLunar.moon_full, cal_events.SAT, months=(3, ))
        swap_spring.times(datetime.time(hour=11), 4)
        self.events.append(swap_spring)

        swap_fall = cal_events.CalEvent(self.eph)
        swap_fall.name = 'Fall Swap Meet'
        swap_fall.visibility = cal_events.EventVisibility.public
        swap_fall.location = cal_events.LOCATIONS[1]
        swap_fall.url = 'www.sjaa.net/events/swap-meet'
        swap_fall.description = ''
        swap_fall.lunar_yearly(
            cal_events.RuleLunar.moon_full, cal_events.SAT, months=(10, ))
        swap_fall.times(datetime.time(hour=11), 4)
        self.events.append(swap_fall)

    def print_events(self, start, until):
        """Generate a summary of all events."""
        public = []
        private = []
        for event in self.events:
            if event.visibility == cal_events.EventVisibility.public:
                for dtstart, _ in event.gen_occurances(start, until):
                    public.append("{0}: {1}".format(
                        event.name,
                        dtstart.strftime('%a %b %-d %Y - %-I:%M %p')))
            else:
                for dtstart, _ in event.gen_occurances(start, until):
                    private.append("{0}: {1}".format(
                        event.name,
                        dtstart.strftime('%a %b %-d %Y - %-I:%M %p')))

        print('*' * 80 + '\n')
        print('\n'.join(public))
        print('*' * 80 + '\n')
        print('\n'.join(private))
        return public, private

    def gen_cal(self, start, until, public):
        """Generate a calendar of public events."""
        cal = icalendar.Calendar()
        if public:
            cal.add('prodid', 'SJAA Public Events Calendar')
            visibility = cal_events.EventVisibility.public,
        else:
            cal.add('prodid', 'SJAA Member Only Events Calendar')
            visibility = (cal_events.EventVisibility.member,
                          cal_events.EventVisibility.private)
        cal.add('version', '2.0')

        for event in self.events:
            if event.visibility in visibility:
                event.add_ical_events(start, until, cal)
        return cal


def write_csv(events, filename, start, until):
    with open('{}.csv'.format(filename), 'w') as cfp:
        cfp = csv.writer(cfp)
        header = ('Event', 'Date', 'Day', 'Type', 'Start Time', 'End Time',
                  'Location')
        cfp.writerow(header)
        for event in events:
            for dtstart, dtend in event.gen_occurances(start, until):
                line = [event.name]
                line.append(dtstart.strftime('%b %-d %Y'))
                line.append(dtstart.strftime('%a'))
                line.append(str(event.visibility).capitalize())
                line.append(dtstart.strftime('%-I:%M %p'))
                line.append(dtend.strftime('%-I:%M %p'))
                line.append(event.location)
                cfp.writerow(line)


# ==============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calendar Generator')
    parser.add_argument(
        '--year',
        type=int,
        action='store',
        required=True,
        help='Year of the generated Calendar')
    parser.add_argument(
        '--public',
        action='store',
        help='Public Events Base Filename',
        default='public')
    parser.add_argument(
        '--private',
        action='store',
        help='Private Events Base Filename',
        default='private')
    args = parser.parse_args()

    # -------------------------------------
    # Actually do the work we intend to do here
    # -------------------------------------
    start = datetime.datetime(args.year, 1, 1)
    until = datetime.datetime(args.year, 12, 31)

    cal_gen = CalGen()
    cal_gen.print_events(start, until)

    public = [
        e for e in cal_gen.events
        if e.visibility == cal_events.EventVisibility.public
    ]
    write_csv(public, args.public, start, until)
    private = [
        e for e in cal_gen.events
        if e.visibility != cal_events.EventVisibility.public
    ]
    write_csv(private, args.private, start, until)

    cal = cal_gen.gen_cal(start, until, public=True)
    with open('{}.ics'.format(args.public), 'wb') as icfp:
        icfp.write(cal.to_ical())

    cal = cal_gen.gen_cal(start, until, public=False)
    with open('{}.ics'.format(args.private), 'wb') as icfp:
        icfp.write(cal.to_ical())
