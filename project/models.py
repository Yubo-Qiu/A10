from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Editor", "Editor"),
        ("Contributor", "Contributor"),
        ("Volunteer", "Volunteer"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="project_profiles"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
        default="profile_images/default-profile.jpg",
    )
    social_links = models.TextField(blank=True)
    contact_email = models.EmailField()
    skills = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def get_absolute_url(self):
        return reverse("profile-detail", args=[self.pk])


class Tag(models.Model):
    name = models.CharField(
        max_length=50, unique=True
    )  # Single word like "impact", "journal", etc.

    def __str__(self):
        return self.name


class Journal(models.Model):
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Published", "Published"),
        ("Archived", "Archived"),
    ]
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)  # Select multiple tags
    featured_image = models.ImageField(
        upload_to="journal_images/", blank=True, null=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("journal-detail", args=[self.pk])


class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ("Software", "Software"),
        ("Community Service", "Community Service"),
        ("Research", "Research"),
        ("Fundraising", "Fundraising"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    collaborators = models.ManyToManyField(Profile, related_name="projects")
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    project_link = models.URLField(blank=True, null=True)
    banner_image = models.ImageField(
        upload_to="project_banners/", blank=True, null=True
    )
    tags = models.ManyToManyField(Tag, blank=True, null=True)  # Tags for projects
    related_blogs = models.ManyToManyField(
        Journal, blank=True, related_name="projects"
    )  # Link to multiple journals

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project-detail", args=[self.pk])


class Collaborator(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="collaborator_logos/", blank=True, null=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    collaboration_type = models.CharField(
        max_length=50,
        choices=[
            ("Sponsor", "Sponsor"),
            ("Partner", "Partner"),
            ("Volunteer Group", "Volunteer Group"),
        ],
    )

    def __str__(self):
        return self.name


class Permission(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Editor", "Editor"),
        ("Volunteer", "Volunteer"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    can_edit_blogs = models.BooleanField(default=False)
    can_edit_projects = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)

    def __str__(self):
        return self.role
