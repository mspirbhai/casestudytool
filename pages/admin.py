from django.contrib import admin

# Register your models here.

from .models import Case, CaseLog

admin.site.register(Case)
admin.site.register(CaseLog)
