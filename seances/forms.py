from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from seances.models import Inscription
from seances.slot import get_incoming_available_slots


class InscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slot"].queryset = get_incoming_available_slots()

    class Meta:
        model = Inscription
        labels = {
            "slot": "Créneau",
        }
        fields = {"slot": forms.ModelChoiceField(queryset=None)}
        widgets = {"slot": forms.RadioSelect}

    def clean(self):
        cleaned_data = super().clean()
        slot = cleaned_data["slot"]
        desired_inscription_date = slot["seance_date"]
        desired_inscription_week_nb = desired_inscription_date.isocalendar()[1]
        member = cleaned_data["member"]
        inscriptions = Inscription.objects.get(member=member)
        for inscription in inscriptions:
            week_nb = inscription["slot"]["seance_date"].isocalendar()[1]
            if week_nb == desired_inscription_week_nb:
                raise ValidationError(
                    "Vous ne pouvez pas vous inscrire à plus d'une séance "
                    "dans la même semaine. Vous pouvez venir au club les "
                    "autres jours si la capacité de la salle le permet. "
                    "Pour savoir si vous pouvez venir sans être inscrit, "
                    "il suffit d'aller voir sur le site le nombre d'inscrits "
                    "au créneau qui vous intéresse."
                )


class FFMELicenseAuthenticationForm(forms.Form):
    ffme_license = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": True}),
        min_length=6,
        max_length=6,
        label="License FFME",
    )
    error_messages = {
        "invalid_login": "License FFME invalide",
        "inactive": "Compte désactivé",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        ffme_license = self.cleaned_data.get("ffme_license")
        if ffme_license is not None:
            self.user_cache = authenticate(
                self.request,
                ffme_license=ffme_license,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )
