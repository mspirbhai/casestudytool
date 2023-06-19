from typing import Any, Optional, Type
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
)

from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from .models import Case, CaseLog, TrackedMetric, Project
from .forms import CaseLogCreateForm, CaseLogUpdateForm


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "pages/projects.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset


class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/about.html"


class CaseListView(LoginRequiredMixin, ListView):
    model = Case
    template_name = "pages/cases.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(project=self.kwargs["pk"])
        return queryset


class CaseCreateView(LoginRequiredMixin, CreateView):
    model = Case
    template_name = "pages/cases_new.html"
    fields = ["name", "description", "project"]

    def get_success_url(self):
        project_id = self.object.project.id
        return reverse_lazy("cases", kwargs={"pk": project_id})


class CaseLogListView(LoginRequiredMixin, ListView):
    model = CaseLog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(case=self.kwargs["pk"])
        return queryset

    template_name = "pages/caselog.html"


class CaseLogDetailView(LoginRequiredMixin, DetailView):
    model = CaseLog
    template_name = "pages/caselog_detail.html"


class CaseLogCreateView(LoginRequiredMixin, CreateView):
    form_class = CaseLogCreateForm
    model = CaseLog
    template_name = "pages/caselog_new.html"
    # fields = ["title", "body", "tracked_value", "tracked_metric"]

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pk"] = self.kwargs["pk"]
        return kw

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.case = Case.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)


"""
    def get_initial(self):
        initial = super().get_initial()
        initial["author"] = self.request.user
        initial["case_name"] = Case.objects.get(pk=self.kwargs["pk"])
        return initial
"""


class CaseLogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = CaseLogUpdateForm
    model = CaseLog
    template_name = "pages/caselog_edit.html"
    # fields = ["title", "body", "tracked_value", "tracked_metric"]

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pk"] = self.kwargs["pk"]
        return kw


class TrackedMetricDetailView(LoginRequiredMixin, DetailView):
    model = TrackedMetric
    template_name = "pages/trackedmetric_detail.html"
