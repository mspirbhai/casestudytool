from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Case


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/about.html"


class CasePageView(LoginRequiredMixin, ListView):
    model = Case
    template_name = "pages/cases.html"
