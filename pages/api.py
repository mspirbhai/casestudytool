from ninja import NinjaAPI, ModelSchema
from ninja.orm import create_schema
from typing import List, Optional
from pages.models import CaseLog, Case, TrackedMetric, Project
from django.contrib.auth import get_user_model

api = NinjaAPI()

User = get_user_model()


class TrackedMetricSchema(ModelSchema):
    class Config:
        model = TrackedMetric
        model_fields = [
            "name",
            "explanation",
            "calculation",
            "units",
        ]


class CaseLogSchema(ModelSchema):
    author: str
    project: str
    case: str
    tracked_value: Optional[str]
    tracked_metric_name: Optional[str]
    tracked_metric_explanation: Optional[str]
    tracked_metric_calculation: Optional[str]
    tracked_metric_units: Optional[str]

    class Config:
        model = CaseLog
        model_fields = [
            "id",
            "case",
            "title",
            "body",
            "author",
        ]

    @staticmethod
    def resolve_author(obj):
        return obj.author.username

    @staticmethod
    def resolve_project(obj):
        return obj.case.project.name

    @staticmethod
    def resolve_case(obj):
        return obj.case.name

    @staticmethod
    def resolve_tracked_value(obj):
        if obj.tracked_value is None:
            return ""
        return str(obj.tracked_value)

    @staticmethod
    def resolve_tracked_metric_name(obj):
        if obj.tracked_metric is None:
            return ""
        return obj.tracked_metric.name

    @staticmethod
    def resolve_tracked_metric_explanation(obj):
        if obj.tracked_metric is None:
            return ""
        return obj.tracked_metric.explanation

    @staticmethod
    def resolve_tracked_metric_calculation(obj):
        if obj.tracked_metric is None:
            return ""
        return obj.tracked_metric.calculation

    @staticmethod
    def resolve_tracked_metric_units(obj):
        if obj.tracked_metric is None:
            return ""
        return obj.tracked_metric.units


@api.get("/hello")
def hello(request):
    return "Hello World!"


@api.get("/caselogs", response=List[CaseLogSchema])
def caselogs(request):
    queryset = CaseLog.objects.all()
    return list(queryset)
