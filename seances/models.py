from django.db import models


class Inscription(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_ca = models.BooleanField()
    seance_date = models.DateField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    ffme_license = models.CharField(max_length=9)
