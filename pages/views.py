from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
)

from .models import Case, CaseLog
from .forms import CaseLogCreateForm


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/about.html"


class CaseListView(LoginRequiredMixin, ListView):
    model = Case
    template_name = "pages/cases.html"


class CaseLogListView(LoginRequiredMixin, ListView):
    model = CaseLog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(case_name=self.kwargs["pk"])
        return queryset

    template_name = "pages/caselog.html"


class CaseLogDetailView(LoginRequiredMixin, DetailView):
    model = CaseLog
    template_name = "pages/caselog_detail.html"


class CaseLogCreateView(LoginRequiredMixin, CreateView):
    form_class = CaseLogCreateForm
    model = CaseLog
    template_name = "pages/caselog_new.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["author"] = self.request.user
        initial["case_name"] = Case.objects.get(pk=self.kwargs["pk"])
        return initial


class CaseLogUpdateView(LoginRequiredMixin, UpdateView):
    model = CaseLog
    template_name = "pages/caselog_edit.html"
    fields = ["title", "body"]
