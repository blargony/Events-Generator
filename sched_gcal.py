



'''
    
'''

# email body header/footer
text_email_body_class_header = '''\
event: {name}
date : {date}
time : {time_start} - {time_end}
place: {location}
'''

text_email_body_class_footer = '''
For more info see:
    {url}
'''

# email body main tet
text_email_body_class_intro = '''\
INTRO CLASS DESCRIPTION HERE.  blah, blah blah
yada, yada, yada
'''

text_email_body_class_101 = '''\
ASTRONOMY 101 CLASS DESCRIPTION HERE.  blah, blah blah
yada, yada, yada
'''

texts = {}
def email_body_init()
    global texts

    # Get all event types
    texts = {}
    evtypes = EventType.filter(pk=t
    for evtype in evtypes:jj
        types[evtype.pk??] = 



def email_body_class_intro(evtype):
    date  = evtype.date.strfmt(FMT_DATE_Y)
    start = evtype.time_start.strfmt(FMT_HM)
    end   = evtype.time_start + evtype.time_length
    end   = end.strfmt(FMT_HM)
    loc   = locations[evtype.location]
    body  = texts[evtype]
    text  = text_email_body_class_header +
            text_email_body_class_intro  +
            text_email_body_class_footer
    return text.format(name=name, date=date, time_start=start,
                       time_end=end, location=loc, url=url)


text_class_101 = '''\n
Google Calendr: ASTRONOMY 101 CLASS text

For more info see:
    {url}
'''


l_location_id = (
        (1, 'abcd'),
        (2, 'stuv')
)


'''
class Announce(TimeStampedModel):
    event_id   = models.ForeignKey(Event, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=2, choices=L_CHANNEL)
    date       = models.DateField()
    Time       = models.TimeField()
    text       = models.CharField(max_length=3000)
    sent       = models.BooleanField(initial=False)
    notes      = models.CharField(max_length=1000)
'''

L_SECTIONS = (
    ('hd', 'header'),
    ('bd', 'body'  ),
    ('ft', 'footer')
)

class AnnounceText(TimeStampedModel):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=2, choices=L_CHANNEL)
    section    = models.CharField(max_length=2, choices=L_SECTION)
    text       = models.CharField(max_length=3000)
    notes      = models.CharField(max_length=1000)

def add_event_channels(event):
    ev_type = event.event_type
    for ch in L_CHANNEL:
        sections = AnnounceText.objects.filter(event_type=ev_type, channel_id=ch)
        if not channel_public[ch] or ev_type.visibilty == EventVisibility.public:
            # skip if channel is not public and event type is not public
            for section in sections:
                section.
