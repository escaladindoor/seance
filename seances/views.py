from django.views.generic.edit import CreateView

from seances.forms import InscriptionForm


class InscriptionView(CreateView):
    form_class = InscriptionForm
    template_name = "inscription.html"
    success_url = "/"
