from django.test import TestCase

from management.forms import WorkerCreationForm
from management.models import Worker, Position, Team


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
