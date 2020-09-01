import datetime

from django.db import models
from django.core.exceptions import ValidationError


class Inscription(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_ca = models.BooleanField()
    seance_date = models.DateField(null=False)
    start = models.TimeField(null=False)
    end = models.TimeField(null=False)
    first_name = models.CharField(max_length=40, null=False)
    last_name = models.CharField(max_length=40, null=False)

    def clean(self):
        if self.end <= self.start:
            raise ValidationError(
                {
                    "end": (
                        "L'heure de fin doit être supérieure (strictement) "
                        "à l'heure de début."
                    )
                }
            )
        if self.start < datetime.time(17):
            raise ValidationError(
                {"start": "L'heure de départ ne peut précéder 17h."}
            )
        if self.end > datetime.time(22):
            raise ValidationError(
                {"end": "L'heure de fin ne peut dépasser 22h."}
            )
        if self.seance_date.weekday() not in (0, 2, 3):
            raise ValidationError(
                {
                    "seance_date": (
                        "La jour de la séance doit être un lundi, "
                        "mercredi ou jeudi."
                    )
                }
            )
