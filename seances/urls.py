from django.urls import path

from seances.views import FFMELicenseLoginView, InscriptionView

urlpatterns = [
    path("", InscriptionView.as_view()),
    path("login/", FFMELicenseLoginView.as_view()),
]
