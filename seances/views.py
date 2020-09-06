from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from seances.forms import (
    InscriptionForm,
    CancellationForm,
    human_readable_date,
    human_readable_time,
)


class InscriptionView(SuccessMessageMixin, CreateView):
    form_class = InscriptionForm
    template_name = "inscription.html"
    success_url = "/"

    def get_success_message(self, cleaned_data):
        msg = (
            "Inscription validée le {seance_date} entre {start} et {end}"
            " pour {first_name} {last_name}"
        )
        return msg.format(
            seance_date=human_readable_date(cleaned_data["seance_date"]),
            start=human_readable_time(cleaned_data["start"]),
            end=human_readable_time(cleaned_data["end"]),
            first_name=cleaned_data["first_name"],
            last_name=cleaned_data["last_name"],
        )

    def get_initial(self):
        """Make the form session-aware"""
        initial = super().get_initial()
        desired_keys = ["first_name", "last_name", "is_ca"]
        for k in desired_keys:
            initial[k] = self.request.session.get(k, None)
        return initial

    def form_valid(self, form):
        desired_keys = ["first_name", "last_name", "is_ca"]
        for k in desired_keys:
            self.request.session[k] = form.cleaned_data[k]
        return super().form_valid(form)


class CancellationView(SuccessMessageMixin, CreateView):
    form_class = CancellationForm
    template_name = "cancellation.html"
    success_url = "/"

    def get_success_message(self, cleaned_data):
        msg = (
            "Inscription annulée le {seance_date} "
            "pour {first_name} {last_name}"
        )
        return msg.format(
            seance_date=human_readable_date(cleaned_data["seance_date"]),
            first_name=cleaned_data["first_name"],
            last_name=cleaned_data["last_name"],
        )

    def get_initial(self):
        """Make the form session-aware"""
        initial = super().get_initial()
        desired_keys = ["first_name", "last_name"]
        for k in desired_keys:
            initial[k] = self.request.session.get(k, None)
        return initial

    def form_valid(self, form):
        desired_keys = ["first_name", "last_name"]
        for k in desired_keys:
            self.request.session[k] = form.cleaned_data[k]
        return super().form_valid(form)
