from django.urls import path

from management.views import (
    index,
    ProjectTypeListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("project-types/", ProjectTypeListView.as_view(), name="project-type-list"),
]

app_name = "management"
