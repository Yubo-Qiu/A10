from django.urls import path
from .views import (
    JournalListView,
    JournalDetailView,
    JournalCreateView,
    JournalUpdateView,
    JournalDeleteView,
    ProfileListView,
    ProfileDetailView,
    HomePageView,
    ProjectListView,
    ProjectDetailView,
    ProfileUpdateView,
    RegisterView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    journals_per_day,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("journals/", JournalListView.as_view(), name="journal-list"),
    path("journals/<int:pk>/", JournalDetailView.as_view(), name="journal-detail"),
    path("journals/new/", JournalCreateView.as_view(), name="journal-create"),
    path(
        "journals/<int:pk>/update/", JournalUpdateView.as_view(), name="journal-update"
    ),
    path(
        "journals/<int:pk>/delete/", JournalDeleteView.as_view(), name="journal-delete"
    ),
    path("profiles/", ProfileListView.as_view(), name="profile-list"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/new/", ProjectCreateView.as_view(), name="project-create"),
    path(
        "projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"
    ),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile-edit"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"
    ),
    path("journals_per_day/", journals_per_day, name="journals_per_day"),
]
