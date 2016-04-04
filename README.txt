README

SJAA Calendar Generator

Run with:
    python3 cal_gen.py

Generates a schedule of events based on rules.  The intent is to correctly
generate a calendar that is at least 90% accurate.  The app does not:
- take into account holidays,
- detect schedule conflicts between events.

Schedule changes need to be done manually. 

Each type of event is described by an instance of the class "EventType".
The generator takes each such instance and generates one or more instances
of class "Event".  Once the events are generated, the app prints the
schedule and, for event with start times based on twilight, sun/moon
ephemeris times.

The output is strictly for viewing purposes.  The app will be enhanced later
to keep a database.


Libraries:
Install modules as follows:
    pip3 install ephem
    pip3 install pytz


files:
    cal_gen.py       - has rules, calls functions to generate schedule
    cal_const.py     - constant values/data structures for app
    cal_events.py    - contains event classes and functions to calculate
                       schedule details
    cal_ephemeris.py - calculates ephemeris data
    cal_opp.py       - calculates opposition times of planets
    sjaa_events_2016.txt - output for 2016
    sjaa_events_2017.txt - output for 2017

    other files for future enhancements
