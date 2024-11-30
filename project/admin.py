from django.contrib import admin
from .models import (
    Profile,
    Journal,
    Project,
    Impact,
    Tag,
    Collaborator,
    Permission,
    MediaGallery,
)


# Customize Admin Displays
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "contact_email")
    search_fields = ("user__username", "role")
    list_filter = ("role",)


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    search_fields = ("title", "author__user__username")
    list_filter = ("status", "tags")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "project_type", "start_date", "end_date")
    search_fields = ("title", "description")
    list_filter = ("project_type",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Impact)
class ImpactAdmin(admin.ModelAdmin):
    list_display = ("title", "impact_type", "related_project", "date")
    search_fields = ("title", "description")
    list_filter = ("impact_type",)


@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ("name", "collaboration_type", "contact_email")
    search_fields = ("name", "collaboration_type")
    list_filter = ("collaboration_type",)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "can_edit_blogs", "can_edit_projects", "can_manage_users")
    list_filter = ("role",)


@admin.register(MediaGallery)
class MediaGalleryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "media_type",
        "upload_date",
        "related_blog",
        "related_project",
    )
    search_fields = ("title", "media_type")
    list_filter = ("media_type",)