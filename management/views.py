from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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
