from django.contrib import admin

# Register your models here.

from .models import Case, CaseLog, TrackedMetric, Project

admin.site.register(Case)
admin.site.register(CaseLog)
admin.site.register(Project)
admin.site.register(TrackedMetric)
