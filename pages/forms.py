from django.forms import ModelForm
from .models import CaseLog, Case, TrackedMetric


class CaseLogCreateForm(ModelForm):
    class Meta:
        model = CaseLog
        fields = ["title", "body", "tracked_value", "tracked_metric"]

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        super().__init__(*args, **kwargs)
        # self.fields["title"].initial = "Test"
        # case_number = int(self.request.path.split("/")[-2:-1].pop())
        case_number = int(self.pk)
        project = Case.objects.get(pk=case_number).project
        project_tracked_metrics = TrackedMetric.objects.filter(project=project)
        self.fields["tracked_metric"].queryset = project_tracked_metrics
        # self.fields["author"].disabled = True


class CaseLogUpdateForm(ModelForm):
    class Meta:
        model = CaseLog
        fields = ["title", "body", "tracked_value", "tracked_metric"]

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        super().__init__(*args, **kwargs)
        caselog_number = int(self.pk)
        case_number = CaseLog.objects.get(pk=caselog_number).case.pk
        project = Case.objects.get(pk=case_number).project
        project_tracked_metrics = TrackedMetric.objects.filter(project=project)
        self.fields["tracked_metric"].queryset = project_tracked_metrics
