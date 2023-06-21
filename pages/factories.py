import factory
from factory.django import DjangoModelFactory

from .models import TrackedMetric, Project, Case, CaseLog
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "username{}".format(n))
    email = factory.Faker("email")
    password = "some_pass"
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class TrackedMetricFactory(DjangoModelFactory):
    class Meta:
        model = TrackedMetric

    name = factory.Faker("word")
    explanation = factory.Faker("sentence")
    calculation = factory.Faker(
        "random_element",
        elements=("SUM", "MEA"),
    )
    units = factory.Faker(
        "random_element",
        elements=("kg", "cm", "m", "kmph", "mph", "bpm", "ohm", "V", "A", "W", "Hz"),
    )
    created_at = factory.Faker("date_time_this_year")
    updated_at = factory.Faker("date_time_this_year")


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker("word")
    case_target = factory.Faker("random_int", min=1, max=100)
    caselog_per_month = factory.Faker("random_int", min=1, max=100)
    created_at = factory.Faker("date_time_this_year")
    updated_at = factory.Faker("date_time_this_year")


class CaseFactory(DjangoModelFactory):
    class Meta:
        model = Case

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    project = factory.Iterator(Project.objects.all())
    created_at = factory.Faker("date_time_this_year")
    updated_at = factory.Faker("date_time_this_year")


class CaseLogFactory(DjangoModelFactory):
    class Meta:
        model = CaseLog

    title = factory.Faker("word")
    case = factory.Iterator(Case.objects.all())
    body = factory.Faker("sentence")
    tracked_value = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=2,
        positive=True,
        min_value=20,
        max_value=100,
    )
    tracked_metric = factory.Iterator(TrackedMetric.objects.all())
    author = factory.Iterator(get_user_model().objects.all())
    created_at = factory.Faker("date_time_this_year")
    updated_at = factory.Faker("date_time_this_year")
