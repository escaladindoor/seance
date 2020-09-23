import collections
import datetime
import itertools
import typing

from seances.models import Slot as SlotModel


class Slot(typing.NamedTuple):
    start: datetime.time
    end: datetime.time


def get_incoming_seance_dates(
    n_days_delta: typing.Optional[int] = 14,
) -> typing.List[datetime.date]:
    seance_dates = list()
    today = datetime.date.today()
    for delta in range(n_days_delta):
        date = today + datetime.timedelta(days=delta)
        if date.weekday() in (0, 2, 3):
            seance_dates.append(date)
    return seance_dates


def get_available_slots_for_date(date: datetime.date) -> typing.List[Slot]:
    if date.weekday() in (0, 2):
        return [
            Slot(datetime.time(17, 30), datetime.time(19)),
            Slot(datetime.time(19), datetime.time(20, 30)),
            Slot(datetime.time(20, 30), datetime.time(22)),
        ]
    if date.weekday() == 3:
        return [Slot(datetime.time(17, 30), datetime.time(20))]
    raise ValueError(f"Invalid weekday: {date.weekday()}")


def get_incoming_available_slots() -> typing.OrderedDict[
    datetime.date, typing.List[Slot]
]:
    pks = list()
    for date in get_incoming_seance_dates():
        for slot in get_available_slots_for_date(date):
            slot_model, _ = SlotModel.objects.get_or_create(
                seance_date=date, start=slot.start, end=slot.end
            )
            if not slot_model.cancelled:
                pks.append(slot_model.pk)
    return SlotModel.objects.filter(pk__in=pks)
