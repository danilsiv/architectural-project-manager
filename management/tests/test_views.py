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


class TeamViewsTests(TestCase):
    def create_worker(
        self, username: str, password: str = "test123user", team: Team = None
    ) -> Worker:
        return Worker.objects.create_user(
            username=username, password=password, position=self.position, team=team
        )

    def create_project(
        self,
        name: str,
        description: str = "test_description",
        deadline: str = "2027-12-12",
        team: Team = None,
    ) -> Project:
        return Project.objects.create(
            name=name,
            description=description,
            deadline=deadline,
            project_type=self.project_type,
            team=team,
        )

    @staticmethod
    def create_team(name: str, team_lead: Worker) -> Team:
        return Team.objects.create(name=name, team_lead=team_lead)

    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position")
        self.project_type = ProjectType.objects.create(name="test_project_type")

        self.team_lead1 = self.create_worker("first_team_lead")
        self.team_1 = self.create_team("first_team", team_lead=self.team_lead1)

        self.worker1 = self.create_worker("first_worker", team=self.team_1)
        self.worker2 = self.create_worker("second_worker", team=self.team_1)

        self.project1 = self.create_project("first_project", team=self.team_1)
        self.project2 = self.create_project("second_project", team=self.team_1)

        self.user = get_user_model().objects.create_user(
            username="test_user", password="test123user", position=self.position
        )
        self.client.force_login(self.user)

    def test_team_list_view(self) -> None:
        self.team_lead2 = self.create_worker("second_team_lead")
        self.team_2 = self.create_team("second_team", team_lead=self.team_lead2)

        teams = Team.objects.order_by("name")
        url = reverse("management:team-list")
        response = self.client.get(url)
        self.assertEqual(list(response.context["team_list"]), list(teams))

    def test_team_detail_view(self) -> None:
        url = reverse("management:team-detail", args=[self.team_1.id])
        response = self.client.get(url)

        self.assertContains(response, self.team_1.name)
        self.assertContains(response, self.team_1.team_lead)

        self.assertContains(response, self.worker1)
        self.assertContains(response, self.worker2)

        self.assertContains(response, self.project1)
        self.assertContains(response, self.project2)

    def test_team_create_view(self) -> None:
        team_lead = self.create_worker("test_team_lead")
        worker = self.create_worker("test_worker")
        project = self.create_project("test_project")

        url = reverse("management:team-create")
        response = self.client.post(
            url,
            {
                "name": "test_team",
                "team_lead": team_lead.id,
                "workers": [worker.id],
                "projects": [project.id],
            },
        )

        self.assertTrue(Team.objects.filter(name="test_team").exists())
        team = Team.objects.get(name="test_team")
        self.assertIn(reverse("management:team-detail", args=[team.id]), response.url)
        self.assertEqual(response.status_code, 302)

    def test_team_update_view(self) -> None:
        team_lead = self.create_worker("updated_team_lead")
        worker = self.create_worker("updated_worker")
        project = self.create_project("updated_project")

        url = reverse("management:team-update", args=[self.team_1.id])
        response = self.client.post(
            url,
            {
                "name": "updated_team_name",
                "team_lead": team_lead.id,
                "members": [worker.id],
                "projects": [project.id],
            },
        )
        self.team_1.refresh_from_db()

        self.assertEqual(self.team_1.name, "updated_team_name")
        self.assertEqual(self.team_1.team_lead, team_lead)
        self.assertEqual(
            list(self.team_1.members.all()),
            list(Worker.objects.filter(username="updated_worker")),
        )
        self.assertEqual(
            list(self.team_1.projects.all()),
            list(Project.objects.filter(name="updated_project")),
        )
        self.assertIn(
            reverse("management:team-detail", args=[self.team_1.id]), response.url
        )
        self.assertEqual(response.status_code, 302)

    def test_team_delete_view(self) -> None:
        url = reverse("management:team-delete", args=[self.team_1.id])
        response = self.client.post(url)

        self.assertFalse(Team.objects.filter(id=self.team_1.id).exists())
        self.assertIn(reverse("management:team-list"), response.url)
        self.assertEqual(response.status_code, 302)
