#########################################################################
#
#   Astronomy Club Event Generator
#   file: cal_ephemeris.py
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
#       2018-07-31  Robert Chapman
#                     - pythonize and add some support methods
#
#########################################################################

import datetime
import math
import unittest

import ephem

from cal_const import *

########################################
# Ephem Constants
########################################
MOON = ephem.Moon()
PLANETS = (ephem.Mars(), ephem.Jupiter(), ephem.Saturn(),
           ephem.Uranus(), ephem.Neptune(), ephem.Pluto())

EPHEM_SECOND = ephem.second
EPHEM_DAY = ephem.hour*24
EPHEM_MONTH = EPHEM_DAY*30

SEASONS = {
    'spring': (ephem.next_vernal_equinox, 'Spring Equinox'),
    'summer': (ephem.next_summer_solstice, 'Summer Solstice'),
    'fall': (ephem.next_autumn_equinox, 'Fall Equinox'),
    'winter': (ephem.next_winter_solstice, 'Winter Solstice')
}

NEXT_MOON_PHASE = {
    #                      method to get phase          , name of phase , next phase
    RuleLunar.moon_new: (ephem.next_new_moon, 'New moon', RuleLunar.moon_1q),
    RuleLunar.moon_1q: (ephem.next_first_quarter_moon, '1st Qtr moon', RuleLunar.moon_full),
    RuleLunar.moon_full: (ephem.next_full_moon, 'Full moon', RuleLunar.moon_3q),
    RuleLunar.moon_3q: (ephem.next_last_quarter_moon, '3rd Qtr moon', RuleLunar.moon_new)
}

########################################
class CalEphemeris(object):
    """Wrap python ephem library for use by cal_events et al."""

    def __init__(self):
        self.observer = ephem.Observer()
        self.observer.lat = LAT
        self.observer.lon = LONG
        self.observer.elevation = ELEVATION

        self.astro_events = []

        # self.gen_astro_data(year)

    # --------------------------------------
    # Ephem to Regular Units Helper Functions
    # --------------------------------------
    def get_datetime(self, ephem_date):
        return ephem.localtime(ephem_date)

    def get_degrees(self, radians):
        return math.degrees(float(radians))

    # --------------------------------------
    # Rising/Setting/Phases/etc...
    # --------------------------------------
    def get_sunset(self, date, horizon=RuleStartTime.sunset):
        self.observer.date = date
        self.observer.horizon = horizon.deg
        return self.get_datetime(self.observer.next_setting(ephem.Sun()))

    def _moon_setup(self, date):
        start_date = date.replace(hour=15, minute=0)
        end_date = start_date + 12 * HOUR    # 3pm to 3am window
        self.observer.date = start_date
        self.observer.horizon = 0
        return start_date, end_date

    def moon_rise(self, date):
        '''Moon rise for a date, around the sunset please.'''
        start_date, end_date = self._moon_setup(date)
        rise = self.get_datetime(self.observer.next_rising(ephem.Moon()))
        if rise > start_date and rise < end_date:
            return rise

    def moon_set(self, date):
        '''Moon set for a date, around the sunset please.'''
        start_date, end_date = self._moon_setup(date)
        set = self.get_datetime(self.observer.next_setting(ephem.Moon()))
        if set > start_date and set < end_date:
            return set

    def moon_illum(self, date):
        date = date.replace(hour=18, minute=0)   # 6pm
        moon = ephem.Moon()
        moon.compute(date)
        return moon.phase

    def get_moon_phase(self, date):
        """Get the Moon Phase around 6pm of any date."""
        date = date.replace(hour=18, minute=0)
        elong = self.get_degrees(ephem.Moon(date).elong)
        # Lean a little bit towards the next phase
        phase = round(elong/90.0) * 90
        if phase == -90:
            return RuleLunar.moon_3q
        elif phase == 0:
            return RuleLunar.moon_new
        elif phase == 90:
            return RuleLunar.moon_1q
        else:
            return RuleLunar.moon_full

    def gen_moon_phases(self, start_date, end_date):
        """Return an interator of moon phases over the given dates."""
        phase_date = start_date
        while phase_date < end_date:
            elong = self.get_degrees(ephem.Moon(phase_date).elong)
            if elong < -90:
                nxt_phase = ephem.next_last_quarter_moon(phase_date)
                phase = str(RuleLunar.moon_3q)
            elif elong < 0:
                nxt_phase = ephem.next_new_moon(phase_date)
                phase = str(RuleLunar.moon_new)
            elif elong < 90:
                nxt_phase = ephem.next_first_quarter_moon(phase_date)
                phase = str(RuleLunar.moon_1q)
            else:
                nxt_phase = ephem.next_full_moon(phase_date)
                phase = str(RuleLunar.moon_full)
            phase_date = self.get_datetime(nxt_phase)
            if phase_date < end_date:
                yield phase, phase_date
            phase_date += DAY

    # --------------------------------------
    def gen_astro_data(self, year):
        """Generate seasons, moon, opposition data for entire year."""

        # Jan 1, midnight, local time
        new_years = datetime.datetime(year, 1, 1, 0, 0)
        new_years = TZ_LOCAL.localize(new_years)
        self.observer.date = new_years.astimezone(TZ_UTC)

        # Generate season data
        for season in SEASONS.keys():
            m, n = SEASONS[season]
            d0 = m(new_years)
            d1 = TZ_LOCAL.localize(ephem.localtime(d0))
            # spaces for formatting
            n = '              ' + n
            self.astro_events.append((d1, n))

        # Generate moon phase events
        cur_year = year - 1
        next_year = year + 1
        ph = RuleLunar.moon_new
        # Generate each successive moon phase event
        # start in December of prior year ("30" days before New Year's Day)
        #   to first phase in next year
        d0 = new_years - DAY*30
        l_moon_phases = []
        while cur_year != next_year:
            prev_ph = ph
            m, n, ph = NEXT_MOON_PHASE[ph]
            d0 = m(d0)
            d1 = TZ_LOCAL.localize(ephem.localtime(d0))
            cur_year = d1.year
            if cur_year == year:
                self.astro_events.append((d1, n))
            l_moon_phases.append((d1, prev_ph))
        # append list of planetary oppositions
        self.astro_events += self.calc_planets(year)
        self.astro_events.sort()


    def calc_date_ephem(self, date):
        """input:

            date - datetime.datetime
        output:
            return string of sun/moon ephemeris for 'date', e.g. for 2016 02/28:
                06:00 PM sunset - 06:28 PM / 06:58 PM / 07:28 PM
                10:06 PM moonrise - 66%
            One of moonrise or moonset is generated, whichever is after 3pm that day.
        """

        # set time for noon
        date = TZ_LOCAL.localize(date.combine(date, datetime.time(12, 0)))
        self.observer.date = date.astimezone(TZ_LOCAL)
        time_sunset = self.get_sunset(date, RuleStartTime.sunset)
        time_civil = self.get_sunset(date, RuleStartTime.civil)
        time_nautical = self.get_sunset(date, RuleStartTime.nautical)
        time_astro = self.get_sunset(date, RuleStartTime.astronomical)
        time_sunset = time_sunset.strftime(FMT_HM)
        time_civil = time_civil.strftime(FMT_HM)
        time_nautical = time_nautical.strftime(FMT_HM)
        time_astro = time_astro.strftime(FMT_HM)
        sun = '{} sunset - {} / {} / {}'.format(time_sunset,
                                                time_civil, time_nautical, time_astro)

    #   print(date.strftime(FMT_YDATE))
    #   MOON.compute('2016/2/28')
        # set time for 3pm
        date = TZ_LOCAL.localize(date.combine(date, datetime.time(15, 0)))
        MOON.compute(date)
        self.observer.date = date.astimezone(TZ_LOCAL)
        self.observer.horizon = RuleStartTime.sunset.deg
        time_moonset = TZ_LOCAL.localize(ephem.localtime(self.observer.next_setting(MOON)))
        # figure out which of moonrise/moonset occurs from 3pm-3am
        if date <= time_moonset < date + HOUR*12:
            moon = '{} moonset'.format(time_moonset.strftime(FMT_HM))
        else:
            time_moonrise = TZ_LOCAL.localize(
                ephem.localtime(self.observer.next_rising(MOON)))
            moon = '{} moonrise'.format(time_moonrise.strftime(FMT_HM))
        moon += ' - {:2.1f}%'.format(MOON.phase)
        return (sun, moon)

    ######################################
    # Calculate Opposition
    ######################################
    def ephem_elong(self, ephem_date, planet):
        planet.compute(ephem_date)
        return planet.elong

    def calc_planets(self, year):
        '''Calculate opposition to solar system objects.

            input
                year    int     year to be considered

            output
                return  list    list of datetime/planet string tuples
        '''
        l_events = []
        for planet in PLANETS:
            date_opp = self.calc_opposition(year, planet)
            if date_opp:
                # spaces for formatting
                event = (date_opp, "                               {} at opposition".format(planet.name))
                l_events.append(event)
        return l_events

    def calc_opposition(self, year, planet):
        '''
        Calculate opposition to solar system object.  Opposition occurs when
        elongation goes from -pi to +pi.

        'ephem.elong' is elongation (angle between object and sun) in radians.
        As string 'ephem.elong' is deg:min:sec.

        Note: Elongation monotonically (?) decreases towards -pi until past
            opposition, at which point elongation jumps to about +pi

        elongation vs time:
                  |\      |\
            \     | \     | \
             \    |  \    |  \
            --\---|---\---|---\-
               \  |    \  |    \
                \ |     \ |
                 \|      \|

        Notes:
        - Times within two minutes of Sky Safari in most cases, but not
          identical.
        - Tried the following, but the calcuated minimum point was off by a
          few minutes:
        http://stackoverflow.com/questions/10146924/finding-the-maximum-of-a-function

        solution = scipy.optimize.minimize_scalar(lambda x: -f(x),
                                                  bounds=[0,1],
                                                  method='bounded')
        - ephem uses 'float' data type to represent time, not datetime

        input
            year    int                 year to be generated
            planet  ephem.<planet>()    planet object

        output
            return  datetime            time of opposition of 'planet'
        '''
        # set start_date as one month before New Year's local time
        # set end_date as one month after New Year's of following year
        new_years = datetime.datetime(year, 1, 1, 0, 0)
        new_years = TZ_LOCAL.localize(new_years)
        start_date = ephem.Date(new_years) - EPHEM_MONTH
        end_date = ephem.Date(new_years) + EPHEM_MONTH*13

        date = start_date
        min_elong      = +4
        min_elong_date = date
        # sample elong every month and find min
        while date < end_date:
            planet.compute(date)
            elong = planet.elong
            if elong < min_elong:
                min_elong      = elong
                min_elong_date = date
            date = ephem.Date(date) + EPHEM_MONTH
        if min_elong_date==start_date or min_elong_date==end_date:
            # min elongation is outside year -> return nothing
            return None
        # elongation the month after opposition should be positive
        end_date       = ephem.Date(min_elong_date) + EPHEM_MONTH
        end_date_elong = self.ephem_elong(end_date, planet)     # should be < 0
        # binary search - find min elongation until interval becomes <= 1 second
        start_date = min_elong_date
        while end_date-start_date > EPHEM_SECOND:
            mid_date       = (start_date + end_date) / 2
            mid_date_elong = self.ephem_elong(mid_date, planet)
            if mid_date_elong > 0:
                end_date   = mid_date
            else:
                start_date = mid_date
            d = ephem.Date(start_date)
        # change 'start_date' to datetime format
        d = ephem.Date(start_date)
        date = ephem.localtime(d)
        date = TZ_LOCAL.localize(date)
        if date.year == year:
            return date
        return None


#########################################################################
class TestUM(unittest.TestCase):

    def setUp(self):
        self.eph = CalEphemeris()
        self.aug = datetime.datetime(2018, 8, 1)
        self.aug_mid = datetime.datetime(2018, 8, 15)
        self.aug_late = datetime.datetime(2018, 8, 31)

    def test_sunset(self):
        # Sunset on August 1, 2018 is 20:16 in San Jose
        sunset = self.eph.get_sunset(self.aug)
        self.assertEqual(sunset.hour, 20)
        self.assertEqual(sunset.minute, 16)

        # nautical sunset should be 21:18
        sunset = self.eph.get_sunset(self.aug, RuleStartTime.nautical)
        self.assertEqual(sunset.hour, 21)
        self.assertEqual(sunset.minute, 21)

    def test_moon_rise(self):
        # Moonrise on August 1, 2018 is 23:10 in San Jose
        rise = self.eph.moon_rise(self.aug)
        self.assertEqual(rise.hour, 23)
        self.assertEqual(rise.minute, 10)
        # Moonrise on August 15, 2018 is in the morning
        rise = self.eph.moon_rise(self.aug_mid)
        self.assertEqual(rise, None)

    def test_moon_set(self):
        # Moonset on August 1, 2018 is not until August 2, 11am
        set = self.eph.moon_set(self.aug)
        self.assertEqual(set, None)
        # Moonset on August 15, 2018 is 11:03pm
        set = self.eph.moon_set(self.aug_mid)
        self.assertEqual(set.hour, 23)
        self.assertEqual(set.minute, 3)

    def test_moon_ill(self):
        # Illuminate for August 1, 2018 is 79%
        ill = self.eph.moon_illum(self.aug)
        self.assertEqual(round(ill), 79)

    def test_moon_phase(self):
        # Phases of the Moon in August
        phases = self.eph.gen_moon_phases(self.aug, self.aug_late)
        phases = list(phases)
        self.assertEqual(len(phases), 4)
        self.assertEqual(phases[0][1].day, 4)
        self.assertEqual(phases[1][1].day, 11)
        self.assertEqual(phases[2][1].day, 18)
        self.assertEqual(phases[3][1].day, 26)
        self.assertEqual(phases[0][0], '3rd Qtr Moon')
        self.assertEqual(phases[1][0], 'New Moon')
        self.assertEqual(phases[2][0], '1st Qtr Moon')
        self.assertEqual(phases[3][0], 'Full Moon')



#########################################################################
if __name__ == '__main__':
    unittest.main()

