from django.urls import path

from management.views import (
    index,
    ProjectTypeListView,
    TeamListView,
    WorkerListView,
    PositionListView,
    ProjectListView,
    TeamDetailView,
    WorkerDetailView,
    ProjectDetailView,
)


urlpatterns = [
    path("", index, name="index"),
    path("project-types/", ProjectTypeListView.as_view(), name="project-type-list"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
]

app_name = "management"
