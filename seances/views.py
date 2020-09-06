from django.views.generic.edit import CreateView

from seances.forms import InscriptionForm


class InscriptionView(CreateView):
    form_class = InscriptionForm
    template_name = "inscription.html"
    success_url = "/"

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
