import io

import pandas as pd
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from seances.models import Member


def load_data(path):
    with open(path, encoding="latin1") as f:
        content = f.read()
    stream = io.StringIO(content)
    d = pd.read_csv(stream, sep=";")
    d = d.rename(
        columns={
            "N.LICENCE": "ffme_license",
            "NOM": "last_name",
            "PRENOM": "first_name",
            "COURRIEL 1": "email",
            "COURRIEL 2": "email_bis",
        }
    )
    d = d.loc[~d.ffme_license.isnull()]
    d["ffme_license"] = d.ffme_license.astype(int).astype(str)
    return d


class Command(BaseCommand):
    help = "Populate database with gym members"

    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, *args, **options):
        path = options["path"]
        data = load_data(path)
        users = list()
        for _, row in data.iterrows():
            user = User(
                username=row.ffme_license,
                email=row.email,
                first_name=row.first_name,
                last_name=row.last_name,
            )
            user.set_unusable_password()
            users.append(user)
        User.objects.bulk_create(users)
