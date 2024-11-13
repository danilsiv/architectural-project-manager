from django.test import TestCase
from django.contrib.auth import get_user_model
from management.models import ProjectType, Position, Project


class ProjectTypeTest(TestCase):
    def test_str_method(self) -> None:
        project_type = ProjectType.objects.create(name="test")
        self.assertEqual(str(project_type), project_type.name)


class WorkerTest(TestCase):
    def test_str_method(self) -> None:
        position = Position.objects.create(name="test")
        worker = get_user_model().objects.create(
            username="test_user",
            password="test123user",
            first_name="test_first",
            last_name="test_last",
            position=position,
        )
        self.assertEqual(
            str(worker),
            f"{worker.first_name} {worker.last_name} ({worker.position.name})",
        )

    def test_create_worker_with_correct_attributes(self) -> None:
        username = "test_user"
        password = "test123user"
        first_name = "test_first"
        last_name = "test_last"
        position = Position.objects.create(name="test")
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            position=position,
        )
        self.assertEqual(worker.username, username)
        self.assertTrue(worker.check_password(password))
        self.assertEqual(worker.first_name, first_name)
        self.assertEqual(worker.last_name, last_name)
        self.assertEqual(worker.position, position)

    def test_absolute_url(self) -> None:
        pass


class PositionTest(TestCase):
    def test_str_method(self) -> None:
        position = Position.objects.create(name="test")
        self.assertEqual(str(position), position.name)


class ProjectTest(TestCase):
    def test_str_method(self) -> None:
        project_type = ProjectType.objects.create(name="test")
        project = Project.objects.create(
            name="test",
            description="test description",
            deadline="2024-12-12",
            project_type=project_type,
        )
        self.assertEqual(str(project), project.name)

    def test_get_absolute_url(self) -> None:
        pass
