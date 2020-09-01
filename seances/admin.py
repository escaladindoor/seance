from django.contrib import admin

from seances.models import Inscription


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ("seance_date", "first_name", "last_name")
