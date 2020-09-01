import datetime

from django import forms
from seances.models import Inscription

def is_seance_date(date):
    return date.weekday in ()

def get_seance_date_choices():
    seance_dates = list()
    today = datetime.date.today()
    for delta in range(14):
        date = today = datetime.timedelta(days=delta)
        if is_seance_date(date):
            seance_dates.append(date)
    return seance_dates


class InscriptionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["seance_dates"].choices = get_seance_date_choices()

    seance_dates = forms.MultipleChoiceField(choices=(), required=True)
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    is_ca = forms.BooleanField()
