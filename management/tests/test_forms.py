from django.test import TestCase

from management.forms import WorkerCreationForm, TeamCreationForm
from management.models import Worker, Position, Team, Project, ProjectType


class WorkerCreationFormTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position")
        self.team_lead_1 = Worker.objects.create_user(
            username="test_user_1", password="test123user", position=self.position
        )
        self.team = Team.objects.create(name="test_team", team_lead=self.team_lead_1)

        self.form_data = {
            "username": "test_user",
            "password1": "some123password",
            "password2": "some123password",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "test@email.com",
            "position": self.position.id,
            "team": self.team.id
        }

    def test_creation_form_data_is_valid(self) -> None:

        form = WorkerCreationForm(data=self.form_data)
        self.form_data["position"] = Position.objects.get(name=self.position.name)
        self.form_data["team"] = Team.objects.get(name=self.team.name)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_update_form_data_is_valid(self) -> None:

        worker = Worker.objects.create_user(
            username=self.form_data["username"],
            password=self.form_data["password1"],
            first_name=self.form_data["first_name"],
            last_name=self.form_data["last_name"],
            email=self.form_data["email"],
            position=self.position,
            team=self.team
        )

        new_position = Position.objects.create(name="new_position")
        team_lead_2 = Worker.objects.create_user(
            username="new_user", password="test123user", position=new_position
        )
        new_team = Team.objects.create(name="new_team", team_lead=team_lead_2)

        updated_data = {
            "username": "updated_username",
            "password1": "some123password",
            "password2": "some123password",
            "first_name": "updated_first_name",
            "last_name": "updated_last_name",
            "email": "updated@email.com",
            "position": new_position.id,
            "team": new_team.id
        }

        form = WorkerCreationForm(data=updated_data, instance=worker)
        form.save()

        updated_data["position"] = Position.objects.get(id=updated_data["position"])
        updated_data["team"] = Team.objects.get(id=updated_data["team"])

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, updated_data)

    def test_form_invalid_when_required_fields_missing(self) -> None:
        self.form_data.pop("username")

        form = WorkerCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_invalid_with_mismatched_password(self) -> None:
        self.form_data["password2"] = "different_password"

        form = WorkerCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_invalid_with_invalid_email(self) -> None:
        self.form_data["email"] = "invalid-email"

        form = WorkerCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_invalid_with_nonexistent_related_objects(self) -> None:
        self.form_data["position"] = 9999
        self.form_data["team"] = 9999

        form = WorkerCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("position", form.errors)
        self.assertIn("team", form.errors)


class TeamCreationFormTests(TestCase):
    def create_worker(self, username: str) -> Worker:
        return Worker.objects.create_user(
            username=username, password="test123user", position=self.position
        )

    def create_project(self, name: str) -> Project:
        return Project.objects.create(
            name=name,
            description="test_description",
            deadline="2027-12-12",
            project_type=self.project_type
        )

    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position")
        self.project_type = ProjectType.objects.create(name="test_project_type")
        self.team_lead = self.create_worker("test_team_lead")
        self.worker_1 = self.create_worker("first_worker")
        self.worker_2 = self.create_worker("second_worker")
        self.project_1 = self.create_project("first_project")
        self.project_2 = self.create_project("second_project")

        self.form_data = {
            "name": "test_team",
            "team_lead": self.team_lead.id,
            "members": [worker.id for worker in Worker.objects.all()],
            "projects": [project.id for project in Project.objects.all()]
        }

    def test_creation_form_data_is_valid(self) -> None:
        form = TeamCreationForm(data=self.form_data)
        self.form_data["team_lead"] = Worker.objects.get(id=self.form_data["team_lead"])
        self.form_data["members"] = Worker.objects.all()
        self.form_data["projects"] = Project.objects.all()

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], self.form_data["name"])
        self.assertEqual(form.cleaned_data["team_lead"], self.form_data["team_lead"])
        self.assertEqual(list(form.cleaned_data["members"]), list(self.form_data["members"]))
        self.assertEqual(list(form.cleaned_data["projects"]), list(self.form_data["projects"]))

    def test_empty_optional_fields(self) -> None:
        self.form_data["members"] = []
        self.form_data["projects"] = []

        form = TeamCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_form_invalid_when_required_fields_missing(self) -> None:
        self.form_data.pop("name")
        self.form_data.pop("team_lead")

        form = TeamCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("team_lead", form.errors)

    def test_form_invalid_with_nonexistent_related_object(self) -> None:
        self.form_data["team_lead"] = 9999
        self.form_data["members"] = [9999, 9999]
        self.form_data["projects"] = [9999, 9999]

        form = TeamCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("team_lead", form.errors)
        self.assertIn("members", form.errors)
        self.assertIn("projects", form.errors)

    def test_team_lead_and_workers_queryset_excludes_admin_and_assigned_workers(self) -> None:
        worker_admin = self.create_worker("worker_admin")
        worker_admin.position = Position.objects.create(name="admin")
        worker_admin.save()

        assigned_worker = self.worker_1
        unassigned_worker = self.worker_2

        team_lead_queryset = TeamCreationForm().fields["team_lead"].queryset
        workers_queryset = TeamCreationForm().fields["members"].queryset
        team = Team.objects.create(name="test_team", team_lead=worker_admin)
        team.members.set([assigned_worker])

        self.assertNotIn(assigned_worker, team_lead_queryset)
        self.assertNotIn(worker_admin, team_lead_queryset)
        self.assertIn(unassigned_worker, team_lead_queryset)
        self.assertEqual(list(team_lead_queryset), list(workers_queryset))

    def test_projects_queryset_excludes_assigned_projects(self) -> None:
        assigned_project = self.project_1
        unassigned_project = self.project_2

        projects_queryset = TeamCreationForm().fields["projects"].queryset
        team = Team.objects.create(name="test_team", team_lead=self.team_lead)
        team.projects.set([assigned_project])

        self.assertNotIn(assigned_project, projects_queryset)
        self.assertIn(unassigned_project, projects_queryset)
