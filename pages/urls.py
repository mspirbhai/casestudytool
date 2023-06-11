from django.urls import path

from .views import (
    HomePageView,
    AboutPageView,
    CaseListView,
    CaseLogListView,
    CaseLogDetailView,
    CaseLogCreateView,
    CaseLogUpdateView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("cases/", CaseListView.as_view(), name="cases"),
    path("cases/<int:pk>/", CaseLogListView.as_view(), name="caselogs"),
    path("caselog/<int:pk>/", CaseLogDetailView.as_view(), name="caselog_detail"),
    path("caselog/new/<int:pk>/", CaseLogCreateView.as_view(), name="caselog_new"),
    path("caselog/edit/<int:pk>/", CaseLogUpdateView.as_view(), name="caselog_edit"),
]
