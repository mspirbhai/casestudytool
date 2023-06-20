from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TrackedMetric(BaseModel):
    class CALC_TYPE(models.TextChoices):
        SUM = "SUM"
        MEAN = "MEA"

    name = models.CharField(max_length=200)
    explanation = models.CharField(max_length=500)
    calculation = models.CharField(
        max_length=3,
        choices=CALC_TYPE.choices,
    )
    units = models.CharField(max_length=10)

    def __str__(self):
        return self.name + " " + self.calculation

    def get_absolute_url(self):
        return reverse("trackedmetric_detail", kwargs={"pk": self.pk})


class Project(BaseModel):
    name = models.CharField(max_length=200)
    case_target = models.IntegerField(blank=True, null=True)
    caselog_per_month = models.IntegerField(blank=True, null=True)
    tracked_metrics = models.ManyToManyField(TrackedMetric, blank=True)
    author = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})


class Case(BaseModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cases", kwargs={"pk": self.pk})


class CaseLog(BaseModel):
    title = models.CharField(max_length=200)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    tracked_value = models.DecimalField(
        max_digits=19, decimal_places=3, null=True, blank=True, default=None
    )
    tracked_metric = models.ForeignKey(
        TrackedMetric,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        default=None,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("caselog_detail", kwargs={"pk": self.pk})

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_both_tracked_values_filled",
                check=(
                    models.Q(
                        tracked_value__isnull=True,
                        tracked_metric__isnull=True,
                    )
                    | models.Q(
                        tracked_value__isnull=False,
                        tracked_metric__isnull=False,
                    )
                ),
            )
        ]
