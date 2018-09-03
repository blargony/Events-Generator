# SJAA Calendar Generator

The Calendar Generator produces a schedule of events based on calendar
rules and the lunar calendar.  (If it just needed to follow the calendar
rules such as 'first Sunday of the Month', 'every Friday', and so onwe
wouldn't need a special application.  The design goal is to produce the
set of events for the year and support pushing these event dates/descriptions
into any calendaring app we may be using.   At the current time, we primarily
use Google Calendars and meetup.com.

The script may produce event dates that may require some manual correction.
Calendars are complicated so a few things may need to be tweaked afterwards.

Possible reasons for changes.
* Avoiding holidays or other events (e.g. solar eclipse day)
* Schedule conflicts between events
* Just because a different date seems better in the judgement of the event coordinator

Each type of event is described by an instance of the class "EventType".
The generator takes each such instance and generates one or more instances
of class "Event".  Once the events are generated, the app prints the
schedule and, for event with start times based on twilight, sun/moon
ephemeris times.


# Support libraries

Check the requirements.txt file but the script relies primarily on
the pyephem module (http://rhodesmill.org/pyephem/) to calculate the
lunar dates and other astro events.

# File overview
* cal_gen.py - Contains the set of event date rules to build a yearly schedule using cal_events
* cal_astro.py - Generates general astro-info (moon phases, illumination sunset times, etc) in CSV and .ICS formats
* cal_events.py - Contains event classes and functions to calculate event date/time details
* cal_holidays.py - Contains methods to help identify if events overlap with US holidays
* cal_ephemeris.py - Wraps the pyephem module to track the dates of moon phases and the times of sunsets and other astro info.
