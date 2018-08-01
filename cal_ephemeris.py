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
import ephem

from cal_const import *

class CalEphemeris(object):
    """Wrap python ephem library for use by cal_event et al."""

    def __init__(self):
        self.observer = ephem.Observer()
        self.observer.lat = LAT
        self.observer.lon = LONG
        self.observer.elevation = ELEVATION

        self.moon_phase = ['']*368
        self.astro_events = []

        # self.gen_astro_data(year)

    def get_sunset(self):
        return TZ_LOCAL.localize(ephem.localtime(self.observer.next_setting(SUN)))

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
        next_phase = {
            #                      method to get phase          , name of phase , next phase
            RuleLunar.moon_new: (ephem.next_new_moon, 'New moon', RuleLunar.moon_1q),
            RuleLunar.moon_1q: (ephem.next_first_quarter_moon, '1st Qtr moon', RuleLunar.moon_full),
            RuleLunar.moon_full: (ephem.next_full_moon, 'Full moon', RuleLunar.moon_3q),
            RuleLunar.moon_3q: (ephem.next_last_quarter_moon, '3rd Qtr moon', RuleLunar.moon_new)
        }
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
            m, n, ph = next_phase[ph]
            d0 = m(d0)
            d1 = TZ_LOCAL.localize(ephem.localtime(d0))
            cur_year = d1.year
            if cur_year == year:
                self.astro_events.append((d1, n))
            l_moon_phases.append((d1, prev_ph))
        # append list of planetary oppositions
        self.astro_events += self.calc_planets(year)
        self.astro_events.sort()

        # populate "moon_phase" with moon phase for every day of year
        ph_time, ph = l_moon_phases.pop(0)
        for e in l_moon_phases:
            next_ph_time, next_ph = e
            delta_ph_time = next_ph_time - ph_time
            # find midpoint between two consecutive lunar events,
            #   e.g., 1Q, full moon
            mid_ph_time = ph_time + delta_ph_time/2
            # append midpoint time
            # use old phase if midpoint is after 7pm, otherwise use new phase
            if mid_ph_time.year == year:
                # day of year, e.g., 201
                mid_ph_day = int(mid_ph_time.strftime('%j'))
                self.moon_phase[mid_ph_day] = ph if mid_ph_time.hour >= 19 else next_ph
            ph_time = next_ph_time
            ph = next_ph
            # fill in "moon_phase" 10 days after midpoint with "ph"
            # 10 days ensures no gap between this midpoint and the next
            for j in range(1, 12):
                day = mid_ph_time + DAY*j
                # don't fill in moon_phase if day is not in current year
                if day.year == year:
                    k = int(day.strftime('%j'))
                    self.moon_phase[k] = ph


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
        self.observer.horizon = rule_horizon[RuleStartTime.sunset]
        time_sunset = TZ_LOCAL.localize(ephem.localtime(self.observer.next_setting(SUN)))
        self.observer.horizon = rule_horizon[RuleStartTime.civil]
        time_civil = TZ_LOCAL.localize(ephem.localtime(self.observer.next_setting(SUN)))
        self.observer.horizon = rule_horizon[RuleStartTime.nautical]
        time_nautical = TZ_LOCAL.localize(ephem.localtime(self.observer.next_setting(SUN)))
        self.observer.horizon = rule_horizon[RuleStartTime.astronomical]
        time_astro = TZ_LOCAL.localize(ephem.localtime(self.observer.next_setting(SUN)))
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
        self.observer.horizon = rule_horizon[RuleStartTime.sunset]
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
