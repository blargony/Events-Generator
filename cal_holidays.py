import datetime
import holidays

from dateutil import rrule

from cal_const import DAY


class CalHoliday(object):

    def __init__(self, date):
        """Initialize for a give year, if you want to be above to iterate."""
        try:
            # Check for a datetime object
            year = date.year
        except AttributeError:
            year = date
        self.hol = holidays.US(years=year)
        self._extra_holidays(year)

    def _extra_holidays(self, year):
        # Add the superbowl, first Sunday in Feb.
        superb_owl = rrule.rrule(rrule.MONTHLY, count=1, byweekday=rrule.SU,
                                 dtstart=datetime.date(year, 2, 1))
        self.hol.append({list(superb_owl)[0]: 'Superbowl Sunday'})

        # Mother's day, Second Sunday in May
        superb_owl = rrule.rrule(rrule.MONTHLY, count=1, byweekday=rrule.SU(2),
                                 dtstart=datetime.date(year, 5, 1))
        self.hol.append({list(superb_owl)[0]: "Mother's Day"})

        # Father's day, Third Sunday in June
        superb_owl = rrule.rrule(rrule.MONTHLY, count=1, byweekday=rrule.SU(3),
                                 dtstart=datetime.date(year, 6, 1))
        self.hol.append({list(superb_owl)[0]: "Father's Day"})

    def get_holidays(self):
        return self.hol.items()

    def holiday_weekend(self, date):
        """Is the given date a near a holiday?"""
        if date.weekday() < 2:
            prev = 3 + date.weekday()   # 3 days prior minimum if Mon-Tues
            next = 2 - date.weekday()   # 1-2 days after for Mon-Tues
        elif date.weekday() > 2:
            prev = date.weekday() - 2   # 1 days prior for Thurs, more for later
            next = 8 - date.weekday()   # 1 day after for Sunday, more for earlier

        for i in range(-1 * prev, next):
            test_date = date + (i * DAY)
            holiday = self.hol.get(test_date)
            if holiday:
                return '{0} ({1})'.format(holiday, test_date.strftime('%b %-d'))


