from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .models import Journal, Profile, Project, Collaborator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Case, When
from django.http import HttpResponseForbidden
from project.utils import has_custom_permission


# List View for Journals
class JournalListView(ListView):
    model = Journal
    template_name = "project/journal_list.html"
    context_object_name = "journals"


# Detail View for Journals
class JournalDetailView(DetailView):
    model = Journal
    template_name = "project/journal_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the permission check to the context
        context["can_edit_blogs"] = has_custom_permission(
            self.request.user, "can_edit_blogs"
        )
        return context


# Create View for Journals
class JournalCreateView(CreateView):
    model = Journal
    template_name = "project/journal_form.html"
    fields = ["title", "content", "tags", "featured_image", "status"]

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has the 'can_edit_blogs' permission
        if not has_custom_permission(request.user, "can_edit_blogs"):
            return HttpResponseForbidden(
                "You do not have permission to create journals."
            )
        return super().dispatch(request, *args, **kwargs)


# Update View for Journals
class JournalUpdateView(UpdateView):
    model = Journal
    template_name = "project/journal_form.html"
    fields = ["title", "content", "tags", "featured_image", "status"]

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has the 'can_edit_blogs' permission
        if not has_custom_permission(request.user, "can_edit_blogs"):
            return HttpResponseForbidden(
                "You do not have permission to create journals."
            )
        return super().dispatch(request, *args, **kwargs)


# Delete View for Journals
class JournalDeleteView(DeleteView):
    model = Journal
    template_name = "project/journal_confirm_delete.html"
    success_url = (
        "/journals/"  # Replace with reverse_lazy('journal-list') if using named URL
    )

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has the 'can_edit_blogs' permission
        if not has_custom_permission(request.user, "can_edit_blogs"):
            return HttpResponseForbidden(
                "You do not have permission to create journals."
            )
        return super().dispatch(request, *args, **kwargs)


# Profile Views
class ProfileListView(ListView):
    model = Profile
    template_name = "project/profile_list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        role_order = Case(
            When(role="Admin", then=1),
            When(role="Editor", then=2),
            When(role="Contributor", then=3),
            When(role="Volunteer", then=4),
        )
        return Profile.objects.all().order_by(role_order, "user__username")


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "project/profile_detail.html"
    context_object_name = "profile"

    def post(self, request, *args, **kwargs):
        profile = self.get_object()  # Get the profile being viewed

        # Check if the logged-in user has the "can_manage_users" permission
        if has_custom_permission(request.user, "can_manage_users"):
            new_role = request.POST.get("role")  # Get the new role from the form
            if new_role in dict(Profile.ROLE_CHOICES).keys():  # Validate the new role
                profile.role = new_role
                profile.save()  # Save the updated role
                return self.get(request, *args, **kwargs)  # Reload the page
        else:
            return HttpResponseForbidden(
                "You do not have permission to manage user roles."
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the permission check to the context
        context["can_manage_users"] = has_custom_permission(
            self.request.user, "can_manage_users"
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "project/profile_form.html"
    fields = ["bio", "profile_image", "social_links", "contact_email", "skills"]
    success_url = reverse_lazy("profile-list")

    def get_object(self):
        return (
            self.request.user.project_profiles.first()
        )  # Get the logged-in user's profile


class ProjectListView(ListView):
    model = Project
    template_name = "project/project_list.html"
    context_object_name = "projects"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(CreateView):
    model = Project
    template_name = "project/project_form.html"
    fields = [
        "title",
        "description",
        "collaborators",
        "project_type",
        "start_date",
        "end_date",
        "project_link",
        "banner_image",
        "tags",
        "related_blogs",
    ]

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has the 'can_edit_projects' permission
        if not has_custom_permission(request.user, "can_edit_projects"):
            return HttpResponseForbidden(
                "You do not have permission to create projects."
            )
        return super().dispatch(request, *args, **kwargs)


# Update View for Projects
class ProjectUpdateView(UpdateView):
    model = Project
    template_name = "project/project_form.html"
    fields = [
        "title",
        "description",
        "collaborators",
        "project_type",
        "start_date",
        "end_date",
        "project_link",
        "banner_image",
        "tags",
        "related_blogs",
    ]

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has the 'can_edit_projects' permission
        if not has_custom_permission(request.user, "can_edit_projects"):
            return HttpResponseForbidden(
                "You do not have permission to update projects."
            )
        return super().dispatch(request, *args, **kwargs)


# Delete View for Projects
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "project/project_confirm_delete.html"
    success_url = reverse_lazy("project-list")

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has the 'can_edit_projects' permission
        if not has_custom_permission(request.user, "can_edit_projects"):
            return HttpResponseForbidden(
                "You do not have permission to delete projects."
            )
        return super().dispatch(request, *args, **kwargs)


# Home Page View
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "project/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["journals"] = Journal.objects.filter(status="Published")[:5]
        context["collaborators"] = Collaborator.objects.all()
        return context


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
