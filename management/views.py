from django.db.models import QuerySet
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
    paginate_by = 15


class TeamListView(generic.ListView):
    model = Team
    queryset = Team.objects.prefetch_related(
        "members").select_related("team_lead__position")
    paginate_by = 10


class TeamDetailView(generic.DetailView):
    model = Team

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related(
            "members__position").select_related("team_lead__position")


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
    paginate_by = 15


class WorkerDetailView(generic.DetailView):
    model = Worker

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(
            "team").select_related("position")


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 15


class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 5


class ProjectDetailView(generic.DetailView):
    model = Project

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(
            "project_type").select_related("team")
