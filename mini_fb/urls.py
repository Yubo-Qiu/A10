from django.urls import path
from .views import ShowProfilePageView
from .views import CreateProfileView
from .views import CreateStatusMessageView
from .views import ShowAllProfilesView
from .views import UpdateProfileView
from .views import DeleteStatusMessageView
from .views import CreateFriendView
from .views import ShowFriendSuggestionsView
from .views import ShowNewsFeedView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>/", ShowProfilePageView.as_view(), name="show_profile"),
    path("create_profile/", CreateProfileView.as_view(), name="create_profile"),
    path("profile/update/", UpdateProfileView.as_view(), name="update_profile"),
    path(
        "status/create_status/", CreateStatusMessageView.as_view(), name="create_status"
    ),
    path(
        "status/<int:pk>/delete/",
        DeleteStatusMessageView.as_view(),
        name="delete_status",
    ),
    path(
        "profile/add_friend/<int:other_pk>/",
        CreateFriendView.as_view(),
        name="add_friend",
    ),
    path("profile/news_feed/", ShowNewsFeedView.as_view(), name="news_feed"),
    path(
        "profile/friend_suggestions/",
        ShowFriendSuggestionsView.as_view(),
        name="friend_suggestions",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="mini_fb/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="mini_fb/logged_out.html"),
        name="logout",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
