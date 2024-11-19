from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from management.models import (
    ProjectType, Team, Worker, Position, Project
)


def index(request: HttpRequest) -> HttpResponse:
    num_project_types = ProjectType.objects.count()
    num_teams = Team.objects.count()
    num_workers = Worker.objects.count()
    num_positions = Position.objects.count()
    num_projects = Project.objects.count()
    context = {
        "num_project_types": num_project_types,
        "num_teams": num_teams,
        "num_workers": num_workers,
        "num_positions": num_positions,
        "num_projects": num_projects,
    }
    return render(
        request, "management/index.html", context=context
    )
