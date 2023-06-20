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

import datetime

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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        projects = Project.objects.all()
        metrics = {}

        for project in projects:
            metrics[project] = {}
            caselogs = CaseLog.objects.filter(case__project=project)
            for tracked in project.tracked_metrics.all():
                total_sum = 0
                total_mean = []
                if tracked.calculation == "SUM":
                    for caselog in caselogs:
                        if (caselog.tracked_value != None) and (
                            caselog.tracked_metric.calculation == "SUM"
                        ):
                            total_sum = total_sum + caselog.tracked_value
                    metrics[project] = metrics[project] | {tracked: total_sum}
                elif tracked.calculation == "MEA":
                    for caselog in caselogs:
                        if (caselog.tracked_value != "None") and (
                            caselog.tracked_metric.calculation == "MEA"
                        ):
                            total_mean.append(caselog.tracked_value)
                    if len(total_mean) != 0:
                        total_mean = sum(total_mean) / len(total_mean)
                    metrics[project] = metrics[project] | {tracked: total_mean}

        context["metrics"] = metrics
        return context


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["date"] = datetime.date(2023, 6, 20)
        return context


class CaseListView(LoginRequiredMixin, ListView):
    model = Case
    template_name = "pages/cases.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["project"] = Project.objects.get(pk=self.kwargs["pk"])
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(project=self.kwargs["pk"])
        return queryset


class CaseCreateView(LoginRequiredMixin, CreateView):
    model = Case
    template_name = "pages/cases_new.html"
    fields = ["name", "description"]

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        project_id = self.object.project.id
        return reverse_lazy("cases", kwargs={"pk": project_id})


class CaseLogListView(LoginRequiredMixin, ListView):
    model = CaseLog

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context["project"] = Case.objects.get(pk=self.kwargs["pk"]).project
        context["case"] = Case.objects.get(pk=self.kwargs["pk"])
        return context

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
