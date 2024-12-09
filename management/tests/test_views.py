from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from management.models import ProjectType, Team, Worker, Position, Project


class LoginRequiredTest(TestCase):
    def setUp(self) -> None:
        project_type = ProjectType.objects.create(name="test_project_type")
        position = Position.objects.create(name="test_position")
        worker = get_user_model().objects.create(
            username="test_user",
            password="test123user",
            position=position
        )
        Project.objects.create(
            name="test_project",
            description="test_description",
            deadline="2026-12-12",
            project_type=project_type,
        )
        Team.objects.create(
            name="test_team",
            team_lead=worker
        )

    def test_main_pages(self) -> None:
        urls = [
            "management:index",
            "management:project-type-list",
            "management:project-type-create",
            "management:team-list",
            "management:team-create",
            "management:worker-list",
            "management:worker-create",
            "management:position-list",
            "management:position-create",
            "management:project-list",
            "management:project-create",
        ]

        for url in urls:
            response = self.client.get(reverse(url))
            self.assertNotEqual(response.status_code, 200)

    def test_pages_with_pk(self) -> None:
        urls = [
            "management:project-type-detail",
            "management:project-type-update",
            "management:project-type-delete",
            "management:team-detail",
            "management:team-update",
            "management:team-delete",
            "management:worker-detail",
            "management:worker-update",
            "management:worker-delete",
            "management:position-detail",
            "management:position-update",
            "management:position-delete",
            "management:project-detail",
            "management:project-update",
            "management:project-delete",
        ]

        for url in urls:
            response = self.client.get(reverse(url, args=[1]))
            self.assertNotEqual(response.status_code, 200)
