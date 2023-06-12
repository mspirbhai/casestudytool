from django.urls import path

from .views import (
    HomePageView,
    AboutPageView,
    CaseListView,
    CaseLogListView,
    CaseLogDetailView,
    CaseLogCreateView,
    CaseLogUpdateView,
    CaseCreateView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("cases/", CaseListView.as_view(), name="cases"),
    path("cases/new/", CaseCreateView.as_view(), name="cases_new"),
    path("cases/<int:pk>/", CaseLogListView.as_view(), name="caselogs"),
    path("caselog/<uuid:pk>/", CaseLogDetailView.as_view(), name="caselog_detail"),
    path("caselog/new/<int:pk>/", CaseLogCreateView.as_view(), name="caselog_new"),
    path("caselog/edit/<uuid:pk>/", CaseLogUpdateView.as_view(), name="caselog_edit"),
]
