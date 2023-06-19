from django.urls import path

from .views import (
    AboutPageView,
    CaseListView,
    CaseLogListView,
    CaseLogDetailView,
    CaseLogCreateView,
    CaseLogUpdateView,
    CaseCreateView,
    TrackedMetricDetailView,
    ProjectListView,
)

urlpatterns = [
    path("", AboutPageView.as_view(), name="about"),
    path("projects/", ProjectListView.as_view(), name="projects"),
    path("cases/<int:pk>/", CaseListView.as_view(), name="cases"),
    path("cases/new/", CaseCreateView.as_view(), name="cases_new"),
    path("caselog/<int:pk>/", CaseLogListView.as_view(), name="caselogs"),
    path(
        "caselog_detail/<int:pk>/", CaseLogDetailView.as_view(), name="caselog_detail"
    ),
    path(
        "trackedmetric/<int:pk>/",
        TrackedMetricDetailView.as_view(),
        name="trackedmetric_detail",
    ),
    path("caselog/new/<int:pk>/", CaseLogCreateView.as_view(), name="caselog_new"),
    path("caselog/edit/<int:pk>/", CaseLogUpdateView.as_view(), name="caselog_edit"),
]
