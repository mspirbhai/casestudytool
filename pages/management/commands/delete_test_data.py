import random

from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ...models import TrackedMetric, Project, Case, CaseLog

User = get_user_model()

NUM_USERS = 4
NUM_TRACKED_METRICS = 5
NUM_PROJECTS = 6
NUM_CASES = 30
NUM_CASELOGS = 200


class Command(BaseCommand):
    help = "Delete test data."

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting test data...")

        models = [User, TrackedMetric, Project, Case, CaseLog]

        for m in models:
            if m is not User:
                m.objects.all().delete()
            else:
                m.objects.filter(is_superuser=False).delete()
