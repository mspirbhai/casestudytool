from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Case(BaseModel):
    case_name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.case_name
