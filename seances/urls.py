from django.urls import path

from seances.views import InscriptionView, CancellationView

urlpatterns = [
    path("", InscriptionView.as_view()),
    path("cancel", CancellationView.as_view()),
]
