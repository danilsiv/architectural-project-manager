from django.contrib import admin

from management.models import Position, ProjectType, Project


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    ordering = ("name", )


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    ordering = ("name", )
