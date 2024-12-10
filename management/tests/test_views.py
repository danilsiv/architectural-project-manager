from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from management.models import ProjectType, Team, Worker, Position, Project


class LoginRequiredTest(TestCase):
    urls_without_pk = [
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
    urls_with_pk = [
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

    def setUp(self) -> None:
        project_type = ProjectType.objects.create(name="test_project_type")
        position = Position.objects.create(name="test_position")
        self.worker = get_user_model().objects.create_user(
            username="test_user", password="test123user", position=position
        )
        Project.objects.create(
            name="test_project",
            description="test_description",
            deadline="2026-12-12",
            project_type=project_type,
        )
        Team.objects.create(name="test_team", team_lead=self.worker)

    def test_redirect_for_unauthenticated_users_without_pk(self) -> None:
        """
        Ensure unauthenticated users are redirected to the login page
        for URLs that do not require a primary key.
        """
        for url in self.urls_without_pk:
            response = self.client.get(reverse(url))
            self.assertNotEqual(response.status_code, 200)
            self.assertIn(reverse("login"), response.url)

    def test_redirect_for_unauthenticated_users_with_pk(self) -> None:
        """
        Ensure unauthenticated users are redirected to the login page
        for URLs that require a primary key.
        """
        for url in self.urls_with_pk:
            response = self.client.get(reverse(url, args=[1]))
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse("login"), response.url)

    def test_success_response_for_authenticated_users_without_pk(self) -> None:
        """
        Ensure authenticated users can access URLs that do not require a primary key.
        """
        self.client.force_login(self.worker)

        for url in self.urls_without_pk:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)

    def test_success_response_for_authenticated_users_with_pk(self) -> None:
        """
        Ensure authenticated users can access URLs that require a primary key.
        """
        self.client.force_login(self.worker)

        for url in self.urls_with_pk:
            response = self.client.get(reverse(url, args=[1]))
            self.assertEqual(response.status_code, 200)


class ProjectTypeViewsTests(TestCase):
    def setUp(self) -> None:
        self.project_type1 = ProjectType.objects.create(name="project_type1")
        self.project_type2 = ProjectType.objects.create(name="project_type2")

        position = Position.objects.create(name="test_position")
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test123user", position=position
        )
        self.client.force_login(self.user)

    def test_project_type_list_view(self) -> None:
        project_types = ProjectType.objects.order_by("name")
        url = reverse("management:project-type-list")
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["project_type_list"]), list(project_types)
        )

    def test_project_type_detail_view(self) -> None:
        url = reverse("management:project-type-detail", args=[self.project_type1.id])
        response = self.client.get(url)
        self.assertContains(response, self.project_type1.name)

    def test_project_type_create_view(self) -> None:
        url = reverse("management:project-type-create")
        response = self.client.post(url, {"name": "test_project_type"})
        self.assertTrue(ProjectType.objects.filter(name="test_project_type").exists())
        project_type = ProjectType.objects.get(name="test_project_type")
        self.assertIn(
            reverse("management:project-type-detail", args=[project_type.id]),
            response.url,
        )
        self.assertEqual(response.status_code, 302)

    def test_project_type_update_view(self) -> None:
        url = reverse("management:project-type-update", args=[self.project_type1.id])
        response = self.client.post(url, {"name": "updated_project_type"})
        self.project_type1.refresh_from_db()
        self.assertEqual(self.project_type1.name, "updated_project_type")
        self.assertIn(
            reverse("management:project-type-detail", args=[self.project_type1.id]),
            response.url,
        )
        self.assertEqual(response.status_code, 302)

    def test_project_type_delete_view(self) -> None:
        url = reverse("management:project-type-delete", args=[self.project_type1.id])
        response = self.client.post(url)
        self.assertFalse(ProjectType.objects.filter(id=self.project_type1.id).exists())
        self.assertIn(reverse("management:project-type-list"), response.url)
        self.assertEqual(response.status_code, 302)
