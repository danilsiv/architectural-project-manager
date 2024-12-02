from django.contrib.auth.forms import UserCreationForm
from django import forms

from management.models import Worker, Team, Project


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
            "team"
        )


class TeamCreationForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.filter(team=None).exclude(
            position__name="admin").select_related("position"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Select Team Members"
    )
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.filter(team=None),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign Projects"
    )
    team_lead = forms.ModelChoiceField(
        queryset=Worker.objects.filter(team=None).exclude(
            position__name="admin").select_related("position")
    )

    class Meta:
        model = Team
        fields = ("name", "team_lead", "members", "projects")

    def __init__(self, *args, **kwargs)  -> None:
        super().__init__(*args, **kwargs)
        if not Worker.objects.filter(team=None).exclude(position__name="admin").exists():
            self.fields["members"].widget = forms.HiddenInput()
            self.no_workers_message = "No available workers to assign."
        else:
            self.no_workers_message = None

        if not Project.objects.filter(team=None).exists():
            self.fields["projects"].widget = forms.HiddenInput()
            self.no_projects_message = "No available projects to assign."
        else:
            self.no_projects_message = None
