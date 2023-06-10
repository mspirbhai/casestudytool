from django.urls import path

from .views import HomePageView, AboutPageView, CasePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("cases/", CasePageView.as_view(), name="cases"),
]
