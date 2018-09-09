import datetime
import holidays
import unittest

from dateutil import rrule


# ==============================================================================
class CalHoliday(object):
    """Holiday wrapper class."""

    def __init__(self, date):
        try:
            # Check for a datetime object
            year = date.year
        except AttributeError:
            year = date
        self.hol = holidays.US(years=year)
        self._extra_holidays(year)

    def _extra_holidays(self, year):
        # Add the superbowl, first Sunday in Feb.
        superb_owl = rrule.rrule(
            rrule.MONTHLY,
            count=1,
            byweekday=rrule.SU,
            dtstart=datetime.date(year, 2, 1))
        self.hol.append({list(superb_owl)[0]: 'Superbowl Sunday'})

        # Mother's day, Second Sunday in May
        superb_owl = rrule.rrule(
            rrule.MONTHLY,
            count=1,
            byweekday=rrule.SU(2),
            dtstart=datetime.date(year, 5, 1))
        self.hol.append({list(superb_owl)[0]: "Mother's Day"})

        # Father's day, Third Sunday in June
        superb_owl = rrule.rrule(
            rrule.MONTHLY,
            count=1,
            byweekday=rrule.SU(3),
            dtstart=datetime.date(year, 6, 1))
        self.hol.append({list(superb_owl)[0]: "Father's Day"})

    def check_date(self, date):
        """Return a holiday if the day passed is one."""
        return self.hol.get(date)

    def get_holidays(self):
        """Return a list of holidays for the year."""
        return self.hol.items()

    def holiday_weekend(self, date):
        """Is the given date a near a holiday?"""
        if date.weekday() < 2:
            prior_days = 3 + date.weekday()  # 3 days prior minimum if Mon-Tues
            post_days = 2 - date.weekday()  # 1-2 days after for Mon-Tues
        elif date.weekday() > 2:
            prior_days = date.weekday(
            ) - 2  # 1 days prior for Thurs, more for later
            post_days = 8 - date.weekday(
            )  # 1 day after for Sunday, more for earlier

        holiday_text = ''
        for i in range(-1 * prior_days, post_days):
            test_date = date + (i * datetime.timedelta(days=1))
            holiday = self.hol.get(test_date)
            if holiday:
                holiday_text = '{0} ({1})'.format(holiday,
                                                  test_date.strftime('%b %-d'))
        return holiday_text


# ==============================================================================
class TestUM(unittest.TestCase):
    def setUp(self):
        self.hol = CalHoliday(2018)

    def test_length(self):
        """14 Holidays in 2018."""
        self.assertEqual(len(self.hol.get_holidays()), 14)

    def test_special(self):
        """SuperBowl - our special addition."""
        date = datetime.datetime(2018, 2, 4)
        self.assertEqual('Superbowl Sunday', self.hol.check_date(date))

    def test_normal(self):
        """Christmas - always a holiday."""
        date = datetime.datetime(2018, 12, 25)
        self.assertEqual('Christmas Day', self.hol.check_date(date))

    def test_weekend(self):
        """Check if a day is near a holiday."""
        date = datetime.datetime(2018, 5, 27)
        self.assertEqual('Memorial Day (May 28)',
                         self.hol.holiday_weekend(date))


# ==============================================================================
if __name__ == '__main__':
    unittest.main()
