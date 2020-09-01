from django.urls import path

from seances.views import InscriptionView

urlpatterns = [
    path("", InscriptionView.as_view()),
]
