from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
import uuid


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TrackedMetric(BaseModel):
    class CALCULATION(models.TextChoices):
        SUM = "SUM"
        MEDIAN = "MED"
        MEAN = "MEA"
        MODE = "MOD"

    name = models.CharField(max_length=200)
    explanation = models.CharField(max_length=500)
    calculation = models.CharField(
        max_length=3,
        choices=CALCULATION.choices,
        default=CALCULATION.SUM,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("trackermetric_detail", kwargs={"pk": self.pk})


class Case(BaseModel):
    case_name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    project = models.ForeignKey(
        "pages.Project", blank=True, null=True, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.case_name

    def get_absolute_url(self):
        return reverse("cases", kwargs={"pk": self.pk})


class CaseLog(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    case_name = models.ForeignKey(Case, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    tracked_value = models.DecimalField(
        max_digits=19, decimal_places=3, null=True, blank=True, default=None
    )
    tracked_description = models.ForeignKey(
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
                        tracked_description__isnull=True,
                    )
                    | models.Q(
                        tracked_value__isnull=False,
                        tracked_description__isnull=False,
                    )
                ),
            )
        ]


class Project(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.case_name
