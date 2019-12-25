"""File containing global contants ."""

from collections import namedtuple

MAILERLITE_API_V2_URL = 'https://api.mailerlite.com/api/v2'

VALID_REQUEST_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

Field = namedtuple('Field', ['key', 'value', 'type'])
Group = namedtuple('Group', ["id", "name", "total", "active", "unsubscribed",
                             "bounced", "unconfirmed", "junk", "sent",
                             "opened", "clicked", "date_created",
                             "date_updated"])
Activity = namedtuple('Activity', ['date', 'report_id', 'subject', 'type',
                                   'link_id', 'link', 'receiver',
                                   'receiver.name', 'receiver.email',
                                   'sender', 'sender.name', 'sender.email'])
Subscriber = namedtuple('Subscriber', ['id', 'name', 'email', 'sent',
                                       'opened', 'clicked', 'type',
                                       'signup_ip', 'signup_timestamp',
                                       'confirmation_ip',
                                       'confirmation_timestamp',
                                       'fields', 'date_subscribe',
                                       'date_unsubscribe', 'date_created',
                                       'date_updated', 'opened_rate',
                                       'clicked_rate', 'country_id'
                                       ])
Pagination = namedtuple('Pagination', ["total", "count", "per_page",
                                       "current_page", "total_pages",
                                       "links"])
Meta = namedtuple('Meta', ['pagination', ])
Segment = namedtuple('Segment', ['id', 'title', 'filter', 'total', 'sent',
                                 'opened', 'clicked', 'created_at',
                                 'updated_at', 'timed_out'])
Stats = namedtuple('Stats', ['count', 'rate'])
Campaign = namedtuple('Campaign', ['id', 'total_recipients', 'type',
                                   'date_created', 'date_send', 'name',
                                   'status', 'opened', 'clicked'])

for nt in [Subscriber, Field, Group, Activity, Segment, Meta, Pagination,
           Campaign, Stats]:
    nt.__new__.__defaults__ = (None,) * len(nt._fields)
