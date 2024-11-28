from django.db.models import QuerySet, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
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
    queryset = ProjectType.objects.annotate(project_count=Count("projects"))
    paginate_by = 15


class ProjectTypeDetailView(generic.DetailView):
    model = ProjectType
    template_name = "management/project_type_detail.html"
    context_object_name = "project_type"


class TeamListView(generic.ListView):
    model = Team
    queryset = Team.objects.select_related(
        "team_lead__position").annotate(member_count=Count("members"))
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
    queryset = Position.objects.exclude(
        name="admin").annotate(worker_count=Count("workers"))
    paginate_by = 15


class PositionDetailView(generic.DetailView):
    model = Position

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related("workers__team")


class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 15


class ProjectDetailView(generic.DetailView):
    model = Project

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(
            "project_type").select_related("team")


class ProjectCreateView(generic.CreateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("management:project-list")
    template_name = "management/project_form.html"


class ProjectUpdateView(generic.UpdateView):
    model = Project
    fields = "__all__"
    template_name = "management/project_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(generic.DeleteView):
    model = Project
    success_url = reverse_lazy("management:project-list")
    template_name = "management/project_confirm_delete.html"
