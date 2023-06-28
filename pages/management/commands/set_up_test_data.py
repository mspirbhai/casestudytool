import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...factories import (
    CaseFactory,
    CaseLogFactory,
    ProjectFactory,
    TrackedMetricFactory,
    UserFactory,
)
from ...models import Case, CaseLog, Project, TrackedMetric

User = get_user_model()

NUM_USERS = 4
NUM_TRACKED_METRICS = 5
NUM_PROJECTS = 6
NUM_CASES = 30
NUM_CASELOGS = 200
USERS_PER_PROJECT = 3
METRICS_PER_PROJECT = 2


class Command(BaseCommand):
    help = "Create test data."

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting test data...")
        models = [User, TrackedMetric, Project, Case, CaseLog]

        for m in models:
            if m is not User:
                m.objects.all().delete()
            else:
                m.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating new data...")

        # Create all the users
        people = []
        for _ in range(NUM_USERS):
            person = UserFactory()
            people.append(person)

        # Create all the tracked metrics
        tracked_metrics = []
        for _ in range(NUM_TRACKED_METRICS):
            tracked_metric = TrackedMetricFactory()
            tracked_metrics.append(tracked_metric)

        # Create all the projects
        projects = []
        for _ in range(NUM_PROJECTS):
            project = ProjectFactory()
            users = random.choices(people, k=USERS_PER_PROJECT)
            users.append(User.objects.get(username="mspirbhai").id)
            tracked = random.choices(tracked_metrics, k=METRICS_PER_PROJECT)
            project.author.set(users)
            project.tracked_metrics.set(tracked)
            projects.append(project)

        # Create all the cases
        cases = []
        for _ in range(NUM_CASES):
            case = CaseFactory()
            cases.append(case)

        # Create all the case logs
        case_logs = []
        for _ in range(NUM_CASELOGS):
            case_log = CaseLogFactory()
            case_logs.append(case_log)
