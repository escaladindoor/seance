import annoying.fields
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from seances.utils import human_readable_date, human_readable_time


class Slot(models.Model):
    seance_date = models.DateField(null=False)
    start = models.TimeField(null=False)
    end = models.TimeField(null=False)
    cancelled = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["seance_date", "start", "end"])]

    def __str__(self):
        return "{date}, entre {start} et {end}".format(
            date=human_readable_date(self.seance_date),
            start=human_readable_time(self.start),
            end=human_readable_time(self.end),
        )


class Member(models.Model):
    user = annoying.fields.AutoOneToOneField(
        User, primary_key=True, on_delete=models.CASCADE
    )
    is_ca = models.BooleanField(default=False)
    email_bis = models.EmailField(blank=True)


class Inscription(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
