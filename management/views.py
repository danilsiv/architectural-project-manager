from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from management.models import (
    ProjectType, Team, Worker, Position, Project
)


def index(request: HttpRequest) -> HttpResponse:
    num_teams = Team.objects.count()
    num_workers = Worker.objects.count()
    num_projects = Project.objects.count()
    context = {
        "num_teams": num_teams,
        "num_workers": num_workers,
        "num_projects": num_projects,
    }
    return render(
        request, "management/index.html", context=context
    )


class ProjectTypeListView(generic.ListView):
    model = ProjectType
    template_name = "management/project_type_list.html"
    context_object_name = "project_type_list"


class TeamListView(generic.ListView):
    model = Team


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")


class PositionListView(generic.ListView):
    model = Position


class ProjectListView(generic.ListView):
    model = Project
