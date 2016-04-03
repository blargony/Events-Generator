# change name of file later?


from django.db   import models
from core.models import TimeStampedModel
# addes "created" "modified" fields

from   cal_const import *

L_CHANNEL  = []

for ch in channels:
    L_CHANNELS.append((ch, channels[ch]))


class AnnounceType(TimeStampedModel):
    event_type  = models.ForeignKey(EventType, on_delete=models.CASCADE)
    channel_id  = models.CharField(max_length=2, choices=L_CHANNEL)
    time_offset = models.DurationField()  # when to send relative to event
    text        = models.CharField(max_length=3000)
    notes       = models.CharField(max_length=1000)

class Announce(TimeStampedModel):
    event_id   = models.ForeignKey(Event, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=2, choices=L_CHANNEL)
    date       = models.DateField()
    text       = models.CharField(max_length=3000)
    sent       = models.BooleanField(initial=False)
    notes      = models.CharField(max_length=1000)

