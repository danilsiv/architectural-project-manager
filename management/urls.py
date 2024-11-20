from django.urls import path

from management.views import (
    index,
    ProjectTypeListView,
    TeamListView,
    WorkerListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("project-types/", ProjectTypeListView.as_view(), name="project-type-list"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list")

]

app_name = "management"
