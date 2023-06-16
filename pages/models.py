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


class Case(BaseModel):
    case_name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    project = models.ForeignKey("pages.Project", blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.case_name

    def get_absolute_url(self):
        return reverse("cases", kwargs={"pk": self.pk})


class CaseLog(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=200)
    case_name = models.ForeignKey("pages.Case", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("caselog_detail", kwargs={"pk": self.pk})

class Project(BaseModel):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.case_name
