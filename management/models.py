from django.contrib.auth.models import AbstractUser
from django.db import models
from architectural_project_manager import settings


class ProjectType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name", )

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        related_name="workers"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self) -> str:
        pass


class Position(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    PRIORITY_CHOICES = [
        ("CR", "Critical"),
        ("HP", "High Priority"),
        ("MP", "Medium Priority"),
        ("LP", "Low Priority"),
        ("BL", "Backlog")
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default="MP"
    )
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    team = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects")

    def get_absolute_url(self) -> str:
        pass

    def __str__(self) -> str:
        return self.name
