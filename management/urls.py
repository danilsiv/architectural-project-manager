from django.urls import path

from management.views import (
    index,
    ProjectTypeListView,
    TeamListView,
    WorkerListView,
    PositionListView,
    ProjectListView,
    TeamDetailView,
)


urlpatterns = [
    path("", index, name="index"),
    path("project-types/", ProjectTypeListView.as_view(), name="project-type-list"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
]

app_name = "management"
