from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
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
        self.caselog = get_object_or_404(CaseLog, pk=self.kwargs["pk"])
        return CaseLog.objects.filter(case_name=self.caselog)

    #    queryset = CaseLog.objects.filter(case_name__pk=self.kwargs["pk"])
    template_name = "pages/caselogs.html"


class CaseLogDetailView(LoginRequiredMixin, DetailView):
    model = CaseLog
    template_name = "pages/caselog_detail.html"
