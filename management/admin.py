from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from management.models import Worker, Position, ProjectType, Project


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    ordering = ("name", )


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    ordering = ("name", )


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "position",
    )
    ordering = ("position", )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "position__name"
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Additional information", {
            "fields": ("position", ),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional information", {
            "fields": ("first_name", "last_name", "email", "position"),
        }),
    )
