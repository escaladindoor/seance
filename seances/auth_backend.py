from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class FFMELicenseAuthBackend(BaseBackend):
    def authenticate(self, request, ffme_license=None):
        try:
            return User.objects.get(username=ffme_license)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
