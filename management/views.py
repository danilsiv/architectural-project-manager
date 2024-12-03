from django.db.models import QuerySet, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from management.models import (
    ProjectType, Team, Worker, Position, Project
)
from management.forms import (
    WorkerCreationForm,
    TeamCreationForm,
    TeamUpdateForm
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

def instruction_view(request: HttpRequest) -> HttpResponse:
    return render(request, "management/instruction.html")


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


class ProjectTypeCreateView(generic.CreateView):
    model = ProjectType
    fields = "__all__"
    template_name = "management/project_type_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:project-type-detail", kwargs={"pk": self.object.pk})


class ProjectTypeUpdateView(generic.UpdateView):
    model = ProjectType
    fields = "__all__"
    template_name = "management/project_type_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:project-type-detail", kwargs={"pk": self.object.pk})


class ProjectTypeDeleteView(generic.DeleteView):
    model = ProjectType
    context_object_name = "project_type"
    success_url = reverse_lazy("management:project-type-list")
    template_name = "management/project_type_confirm_delete.html"


class TeamListView(generic.ListView):
    model = Team
    queryset = Team.objects.select_related(
        "team_lead__position").annotate(member_count=Count("members"))
    paginate_by = 10


class TeamDetailView(generic.DetailView):
    model = Team

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related(
            "members__position", "projects").select_related("team_lead__position")


class TeamCreateView(generic.CreateView):
    model = Team
    form_class = TeamCreationForm
    template_name = "management/team_form.html"

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        team = self.object

        form.cleaned_data["members"].update(team=team)
        form.cleaned_data["projects"].update(team=team)

        return response

    def get_success_url(self) -> str:
        return reverse_lazy("management:team-detail", kwargs={"pk": self.object.pk})


class TeamUpdateView(generic.UpdateView):
    model = Team
    form_class = TeamUpdateForm
    template_name = "management/team_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(generic.DeleteView):
    model = Team
    template_name = "management/team_confirm_delete.html"
    success_url = reverse_lazy("management:team-list")


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.exclude(position__name="admin").select_related("position")
    paginate_by = 15


class WorkerDetailView(generic.DetailView):
    model = Worker

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(
            "team").select_related("position")


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm

    def get_success_url(self) -> str:
        return reverse_lazy("management:worker-detail", kwargs={"pk": self.object.pk})


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    fields = ("username", "first_name", "last_name", "email", "position", "team")
    template_name = "management/worker_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("management:worker-list")
    template_name = "management/worker_confirm_delete.html"


class PositionListView(generic.ListView):
    model = Position
    queryset = Position.objects.exclude(
        name="admin").annotate(worker_count=Count("workers"))
    paginate_by = 15


class PositionDetailView(generic.DetailView):
    model = Position

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related("workers__team")

class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    template_name = "management/position_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:position-detail", kwargs={"pk": self.object.pk})


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    template_name = "management/position_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:position-detail", kwargs={"pk": self.object.pk})


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("management:position-list")
    template_name = "management/position_confirm_delete.html"


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
    template_name = "management/project_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:project-detail", kwargs={"pk": self.object.pk})


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
