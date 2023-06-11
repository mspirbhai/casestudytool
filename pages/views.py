from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView

from .models import Case, CaseLog


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/about.html"


class CaseListView(LoginRequiredMixin, ListView):
    model = Case
    template_name = "pages/cases.html"


class CaseLogListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        queryset = CaseLog.objects.filter(case_name=self.kwargs["pk"])
        return queryset

    template_name = "pages/caselog.html"


class CaseLogDetailView(LoginRequiredMixin, DetailView):
    model = CaseLog
    template_name = "pages/caselog_detail.html"
