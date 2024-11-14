from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from management.models import Position, ProjectType


class AdminPositionTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123admin"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="test_position")

    def test_position_name_should_be_in_search_field(self) -> None:
        """
        Test that position's name is in search_field on position's list page
        """
        url = reverse("admin:management_position_changelist")
        response = self.client.get(url, {"q": self.position.name})
        self.assertContains(response, self.position.name)


class AdminProjectTypeTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123admin"
        )
        self.client.force_login(self.admin_user)
        self.project_type = ProjectType.objects.create(name="test_project_type")

    def test_project_type_name_should_be_in_search_field(self) -> None:
        """
        Test that name of project type is in search_field on
        list page of project types
        :return:
        """
        url = reverse("admin:management_projecttype_changelist")
        response = self.client.get(url)
        self.assertContains(response, "name")


class AdminWorkerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123admin"
        )
        self.client.force_login(self.admin_user)
        position = Position.objects.create(name="test_position")
        self.worker = get_user_model().objects.create_user(
            username="test_user",
            password="test123user",
            first_name="test_first",
            last_name="test_last",
            email="worker@test.com",
            position=position
        )

    def test_worker_attributes_listed(self) -> None:
        """
        Test that worker's username, email, position is correctly
        displayed in list_display
        """
        url = reverse("admin:management_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.username)
        self.assertContains(response, self.worker.email)
        self.assertContains(response, self.worker.position.name)


    def test_get_full_name_method(self) -> None:
        """
        Test that get_full_name is correctly displayed in list_display
        """
        url = reverse("admin:management_worker_changelist")
        response = self.client.get(url)
        expected_result = f"{self.worker.first_name} {self.worker.last_name}"
        self.assertContains(response, expected_result)

    def test_worker_attributes_in_search_field(self) -> None:
        """
        Test that worker's username, first_name, last_name, position
        is in search_field on worker's list_page
        """
        url = reverse("admin:management_worker_changelist")

        params = (
            self.worker.username,
            self.worker.first_name,
            self.worker.last_name,
            self.worker.position.name
        )

        for param in params:
            response = self.client.get(url, {"q": param})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, param)


    def test_worker_detail_position_listed(self) -> None:
        """
        Test that worker's position is on worker detail admin page
        """
        url = reverse("admin:management_worker_change", args=[self.worker.id])
        response = self.client.get(url)
        self.assertContains(response, self.worker.position.name)

    def test_worker_create_attributes_listed(self) -> None:
        """
        Test that worker's first_name, last_name, email, position
        is on worker admin page
        """
        url = reverse("admin:management_worker_add")
        response = self.client.get(url)

        fields = (
            'name="first_name"',
            'name="last_name"',
            'name="email"',
            'name="position"'
        )

        for field in fields:
            self.assertContains(response, field)
