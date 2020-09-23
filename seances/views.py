import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from seances.forms import FFMELicenseAuthenticationForm, InscriptionForm
from seances.models import Member
from seances.utils import human_readable_date, human_readable_time


class InscriptionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = InscriptionForm
    template_name = "inscription.html"
    success_url = "/"
    login_url = "/login/"

    def get_success_message(self, cleaned_data):
        msg = (
            "Inscription validée le {seance_date} entre {start} et {end}"
            " pour {first_name} {last_name}"
        )
        return msg.format(
            seance_date=human_readable_date(cleaned_data["slot"].date),
            start=human_readable_time(cleaned_data["slot"].start),
            end=human_readable_time(cleaned_data["slot"].end),
            first_name=cleaned_data["user"].first_name,
            last_name=cleaned_data["user"].last_name,
        )

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.member = Member.objects.get(user=self.request.user)
        return super().form_valid(form)


class FFMELicenseLoginView(LoginView):
    template_name = "login.html"
    authentication_form = FFMELicenseAuthenticationForm
