# change name of file later?


from django.db   import models
from core.models import TimeStampedModel
# addes "created" "modified" fields

from   cal_const import *

L_VISIBILITY  = []
L_REPEAT      = []
L_LUNAR_PHASE = []
L_WEEK        = []
L_WEEKDAY     = []
L_STARTTIME   = []
L_LOCATION    = []

lists = (
         (EventVisibility, event_visibility, L_VISIBILITY   ),
         (EventRepeat    , event_repeat    , L_REPEAT       )
         (RuleLunar      , rule_lunar      , L_LUNAR_PHASE  ),
         (RuleWeek       , rule_week       , L_WEEK         ),
         (RuleWeekday    , RuleWeekday     , L_WEEKDAY      ),
         (RuleStartTime  , rule_start_time , L_STARTTIME),
)

for rule, rule_strings, choice in lists:
    for item in rule:
        choice.append((item, rule_strings[item]))

for loc in locations:
    L_LOCATIONS.append((loc, locations[loc]))


class EventType(TimeStampedModel):
    name              = models.CharField(max_length=30)
    visibility        = models.CharField(max_length=2, choices=L_VISIBILITY)
    repeat            = models.CharField(max_length=2, choices=L_REPEAT)
    lunar_phase       = models.CharField(max_length=2, choices=L_LUNAR_PHASE,            blank=True)
    week              = models.CharField(max_length=2, choices=L_WEEK       ,            blank=True)
    weekday           = models.CharField(max_length=2, choices=L_WEEKDAY    ,            blank=True)
    time_start        = models.TimeField(                                     null=True, blank=True)
    time_start_offset = models.DurationField(                                 null=True, blank=True)
    time_earliest     = models.TimeField(                                     null=True, blank=True)
    time_length       = models.DurationField(                                 null=True, blank=True)
    location          = models.CharField(max_length=2, choices=L_LOCATION   ,            blank=True)
    tentative         = models.BooleanField(initial=False)
#   hide_loc          = models.BooleanField(initial=False)  # ???
    coordinator       = models.IntegerField(choices??)  # one-to-many ForeignKey ??
    url               = models.CharField(max_length=30)
    notes             = models.CharField(max_length=1000)



class Event(TimeStampedModel):
    event_type    = models.ForeignKey(EventType), on_delete=models.CASCADE)
    name          = models.CharField(max_length=30)
    visibility    = models.CharField(max_length=2, choices=L_VISIBILITY)
    date          = models.DateField(                                              )
    time_start    = models.TimeField(                                     null=True)
    time_length   = models.DurationField(                                 null=True)
    location      = models.CharField(max_length=2, choices=L_LOCATION   , null=True)
    tentative     = models.BooleanField(initial=False)
#   hide_loc      = models.BooleanField(initial=False)  # ???
    coordinator   = models.IntegerField(choices)  # one-to-many ForeignKey ??
    url           = models.CharField(max_length=30)
    notes         = models.CharField(max_length=1000)


'''
    if repeat==LUNAR and lunar_phase or

    if time_start and not time_length or not time_start and time_length
'''
