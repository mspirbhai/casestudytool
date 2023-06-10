from django.db import models
from django.utils import timezone
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Case(BaseModel):
    case_name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.case_name


class CaseLog(BaseModel):
    title = models.CharField(max_length=200)
    case_name = models.ForeignKey("pages.Case", on_delete=models.CASCADE)
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("case_detail", kwargs={"pk": self.pk})
