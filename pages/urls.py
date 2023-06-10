from django.urls import path

from .views import (
    HomePageView,
    AboutPageView,
    CaseListView,
    CaseLogListView,
    CaseLogDetailView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("cases/", CaseListView.as_view(), name="cases"),
    path("cases/<int:pk>/", CaseLogListView.as_view(), name="caselogs"),
    path("caselogs/<int:pk>/", CaseLogDetailView.as_view(), name="caselog_detail"),
]
