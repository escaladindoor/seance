from django.contrib import admin

from seances.models import Inscription, Member, Slot
from seances.utils import human_readable_date


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ("slot", "member")


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    def my_seance_date(self, obj):
        return human_readable_date(obj.seance_date)

    list_display = ("my_seance_date", "start", "end")


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("user", "is_ca", "email_bis")
