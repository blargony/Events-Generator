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
import datetime

from cal_const import EventVisibility, RuleLunar, RuleStartTime, LOCATIONS
import cal_events
import cal_ephemeris


class CalGen():

    def __init__(self, year):
        start = datetime.datetime(year, 1, 1)
        until = datetime.datetime(year + 1, 12, 31)

        self.eph = cal_ephemeris.CalEphemeris(start, until)
        self.year = year

        self.events = []
        self.init_events()

    def init_events(self):
        import pprint
        pp = pprint.PrettyPrinter(width=120)

        class_intro = cal_events.CalEvent(self.eph, self.year)
        class_intro.name = 'Intro to the Night Sky'
        class_intro.visibility = EventVisibility.public
        class_intro.location = LOCATIONS[1]
        class_intro.url = 'www.sjaa.net/programs/beginners-astronomy'
        class_intro.description = ''
        class_intro.lunar(RuleLunar.moon_1q, cal_events.FRI)
        class_intro.sunset_times(
            RuleStartTime.nautical, datetime.time(hour=19), -1, 1)
        self.events.append(class_intro)
        pp.pprint(class_intro.gen_occurances())

        class_101 = cal_events.CalEvent(self.eph, self.year)
        class_101.name = 'Astronomy 101'
        class_101.visibility = EventVisibility.public
        class_101.location = LOCATIONS[1]
        class_101.url = 'www.sjaa.net/programs/beginners-astronomy'
        class_101.description = ''
        class_101.lunar(RuleLunar.moon_3q, cal_events.FRI)
        class_101.sunset_times(
            RuleStartTime.nautical, datetime.time(hour=19), -1, 1)
        self.events.append(class_101)

        itsp_1q = cal_events.CalEvent(self.eph, self.year)
        itsp_1q.name = 'In-town Star Party'
        itsp_1q.visibility = EventVisibility.public
        itsp_1q.location = LOCATIONS[2]
        itsp_1q.url = 'www.sjaa.net/events/monthly-star-parties'
        itsp_1q.description = '1st quarter moon ITSP'
        itsp_1q.lunar(RuleLunar.moon_3q, cal_events.FRI)
        itsp_1q.sunset_times(
            RuleStartTime.nautical, datetime.time(hour=19), 0, 3)
        self.events.append(itsp_1q)

        itsp_3q = cal_events.CalEvent(self.eph, self.year)
        itsp_3q.name = 'In-town Star Party'
        itsp_3q.visibility = EventVisibility.public
        itsp_3q.location = LOCATIONS[2]
        itsp_3q.url = 'www.sjaa.net/events/monthly-star-parties'
        itsp_3q.description = '3rd quarter moon ITSP'
        itsp_3q.lunar(RuleLunar.moon_3q, cal_events.FRI)
        itsp_3q.sunset_times(
            RuleStartTime.nautical, datetime.time(hour=19), 0, 3)
        self.events.append(itsp_3q)

        starry_night = cal_events.CalEvent(self.eph, self.year)
        starry_night.name = 'Starry Night (OSA)'
        starry_night.visibility = EventVisibility.public
        starry_night.location = LOCATIONS[3]
        starry_night.url = 'www.sjaa.net/events/starry-nights-public-star-party/'
        starry_night.description = ''
        starry_night.lunar(RuleLunar.moon_3q, cal_events.SAT)
        starry_night.sunset_times(
            RuleStartTime.civil, None, 0, 3)
        self.events.append(starry_night)

        dark_sky = cal_events.CalEvent(self.eph, self.year)
        dark_sky.name = 'Dark Sky Night'
        dark_sky.visibility = EventVisibility.member
        dark_sky.location = LOCATIONS[4]
        dark_sky.url = 'www.sjaa.net/dark-sky-nights??'
        dark_sky.description = ''
        dark_sky.lunar(RuleLunar.moon_new, cal_events.SAT)
        dark_sky.sunset_times(
            RuleStartTime.civil, datetime.time(hour=19), 0, 4)
        self.events.append(dark_sky)

        quick_start = cal_events.CalEvent(self.eph, self.year)
        quick_start.name = 'Quick STARt'
        quick_start.visibility = EventVisibility.private
        quick_start.location = LOCATIONS[1]
        quick_start.url = 'www.sjaa.net/programs/quick-start'
        quick_start.description = ''
        quick_start.lunar(RuleLunar.moon_1q, cal_events.SAT)
        quick_start.sunset_times(
            RuleStartTime.absolute, datetime.time(hour=19), 0, 3)
        self.events.append(quick_start)

        solar_sunday = cal_events.CalEvent(self.eph, self.year)
        solar_sunday.name = 'Solar Sunday'
        solar_sunday.visibility = EventVisibility.public
        solar_sunday.location = LOCATIONS[1]
        solar_sunday.url = 'www.sjaa.net/solar-observing??'
        solar_sunday.description = ''
        solar_sunday.monthly(1, cal_events.SUN)
        solar_sunday.times(datetime.time(hour=13), 2)
        self.events.append(solar_sunday)

        fix_it = cal_events.CalEvent(self.eph, self.year)
        fix_it.name = 'Fix It'
        fix_it.visibility = EventVisibility.public
        fix_it.location = LOCATIONS[2]
        fix_it.url = 'www.sjaa.net/programs/fix-it'
        fix_it.description = ''
        fix_it.monthly(1, cal_events.SUN)
        fix_it.times(datetime.time(hour=14), 2)
        self.events.append(fix_it)
        pp.pprint(fix_it.gen_occurances())

        image_sig = cal_events.CalEvent(self.eph, self.year)
        image_sig.name = 'Imaging SIG'
        image_sig.visibility = EventVisibility.public
        image_sig.location = LOCATIONS[1]
        image_sig.url = 'www.sjaa.net/programs/imaging-sig'
        image_sig.description = ''
        image_sig.monthly(3, cal_events.TUE)
        image_sig.times(datetime.time(hour=19, minute=30), 2)
        self.events.append(image_sig)

        board_mtg = cal_events.CalEvent(self.eph, self.year)
        board_mtg.name = 'Board Meeting'
        board_mtg.visibility = EventVisibility.member
        board_mtg.location = LOCATIONS[1]
        board_mtg.url = 'www.sjaa.net/board-meeting??'
        board_mtg.description = ''
        board_mtg.lunar(RuleLunar.moon_full, cal_events.SAT)
        board_mtg.times(datetime.time(hour=18), 2)
        self.events.append(board_mtg)

        gen_mtg = cal_events.CalEvent(self.eph, self.year)
        gen_mtg.name = 'General Meeting'
        gen_mtg.visibility = EventVisibility.public
        gen_mtg.location = LOCATIONS[1]
        gen_mtg.url = 'www.sjaa.net/programs/monthly-guest-speakers'
        gen_mtg.description = ''
        gen_mtg.lunar_yearly(RuleLunar.moon_full, cal_events.SAT,
                             months=(1, 3, 4, 5, 6, 7, 10, 11, 12))  # Skip special meetings
        gen_mtg.times(datetime.time(hour=19, minute=30), 2)
        self.events.append(gen_mtg)

        mem_mtg = cal_events.CalEvent(self.eph, self.year)
        mem_mtg.name = 'Membership Meeting/Awards Night'
        mem_mtg.visibility = EventVisibility.member
        mem_mtg.location = LOCATIONS[1]
        mem_mtg.url = 'www.sjaa.net/membership-meeting??'
        mem_mtg.description = ''
        mem_mtg.lunar_yearly(RuleLunar.moon_full, cal_events.SAT, months=(2,))
        mem_mtg.times(datetime.time(hour=19, minute=30), 2)
        self.events.append(mem_mtg)

        movie_night = cal_events.CalEvent(self.eph, self.year)
        movie_night.name = 'Movie Night'
        movie_night.visibility = EventVisibility.member
        movie_night.location = LOCATIONS[1]
        movie_night.url = 'www.sjaa.net/movie-night'
        movie_night.description = 'Member Only Movie Night'
        movie_night.lunar_yearly(RuleLunar.moon_full, cal_events.SAT, months=(8,))
        movie_night.times(datetime.time(hour=19, minute=30), 2)
        self.events.append(movie_night)

        show_n_tell = cal_events.CalEvent(self.eph, self.year)
        show_n_tell.name = '*Show-n-tell'
        show_n_tell.visibility = EventVisibility.public
        show_n_tell.location = LOCATIONS[1]
        show_n_tell.url = 'www.sjaa.net/events/show-n-tell??'
        show_n_tell.description = ''
        show_n_tell.lunar_yearly(RuleLunar.moon_full, cal_events.SAT, months=(9,))
        show_n_tell.times(datetime.time(hour=19, minute=30), 2)
        self.events.append(show_n_tell)

        swap_spring = cal_events.CalEvent(self.eph, self.year)
        swap_spring.name = '*Spring Swap Meet'
        swap_spring.visibility = EventVisibility.public
        swap_spring.location = LOCATIONS[1]
        swap_spring.url = 'www.sjaa.net/events/swap-meet'
        swap_spring.description = ''
        swap_spring.lunar_yearly(RuleLunar.moon_full, cal_events.SAT, months=(3,))
        swap_spring.times(datetime.time(hour=11), 4)
        self.events.append(swap_spring)

        swap_fall = cal_events.CalEvent(self.eph, self.year)
        swap_fall.name = '*Fall Swap Meet'
        swap_fall.visibility = EventVisibility.public
        swap_fall.location = LOCATIONS[1]
        swap_fall.url = 'www.sjaa.net/events/swap-meet'
        swap_fall.description = ''
        swap_fall.lunar_yearly(RuleLunar.moon_full, cal_events.SAT, months=(10,))
        swap_fall.times(datetime.time(hour=11), 4)
        self.events.append(swap_fall)


# ==============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calendar Generator')
    parser.add_argument('--year', type=int, action='store', required=True,
                        help='Year of the generated Calendar')
    parser.add_argument('--test', action='store',
                        help='Test')
    args = parser.parse_args()

    # -------------------------------------
    # Actually do the work we intend to do here
    # -------------------------------------
    cal_gen = CalGen(args.year)
    # summary = cal_gen.gen_events()

    if not args.test:
        pass
        # print('\n'.join(summary))
    else:
        fail = False
        with open(args.test, 'r') as fp:
            for i, line in enumerate(fp):
                if line.rstrip() != summary[i]:
                    print('Golden : {}'.format(line.rstrip()))
                    print('Current: {}'.format(summary[i]))
                    fail = True
        if not fail:
            print('PASS!!')
