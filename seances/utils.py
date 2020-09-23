import datetime

from django.template.defaultfilters import date as _date


def human_readable_date(date: datetime.date):
    return _date(date, "D j N")


def human_readable_time(time: datetime.time):
    return time.strftime("%H:%M")
