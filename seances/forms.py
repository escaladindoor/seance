import datetime
import locale

from django import forms
from django.template.defaultfilters import date as _date

from seances.models import Cancellation, Inscription


def human_readable_date(date: datetime.date):
    return _date(date, "D j N")


def human_readable_time(time: datetime.time):
    return time.strftime("%H:%M")


def get_seance_date_choices():
    seance_dates = list()
    today = datetime.date.today()
    for delta in range(14):
        date = today + datetime.timedelta(days=delta)
        if date.weekday() in (0, 2, 3):
            seance_dates.append((date, human_readable_date(date)))
    return tuple(seance_dates)


def get_time_choices():
    choices = list()
    today = datetime.date.today()
    t = datetime.datetime.combine(today, datetime.time(16, 30))
    max = datetime.datetime.combine(today, datetime.time(22, 0))
    while t < max:
        t += datetime.timedelta(minutes=30)
        choices.append((t.time(), human_readable_time(t.time())))
    return tuple(choices)


class InscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["seance_date"].widget.choices = get_seance_date_choices()

    class Meta:
        model = Inscription
        fields = [
            "first_name",
            "last_name",
            "seance_date",
            "start",
            "end",
            "is_ca",
        ]
        widgets = {
            "seance_date": forms.Select(choices=()),
            "start": forms.Select(choices=get_time_choices()),
            "end": forms.Select(choices=get_time_choices()),
        }
        labels = {
            "seance_date": "Date de la séance",
            "first_name": "Prénom",
            "last_name": "Nom",
            "is_ca": "Membre du CA ?",
            "start": "Heure de début de séance",
            "end": "Heure de fin de séance",
        }


class CancellationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["seance_date"].widget.choices = get_seance_date_choices()

    class Meta:
        model = Cancellation
        fields = [
            "first_name",
            "last_name",
            "seance_date",
        ]
        widgets = {
            "seance_date": forms.Select(choices=()),
        }
        labels = {
            "seance_date": "Date de la séance",
            "first_name": "Prénom",
            "last_name": "Nom",
        }
