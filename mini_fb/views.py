from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from .forms import CreateProfileForm
from .forms import CreateStatusMessageForm
from .forms import UpdateProfileForm
from .models import Profile
from .models import StatusMessage, Image
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


class ShowAllProfilesView(ListView):
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"


class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def form_valid(self, form):
        # Reconstruct the UserCreationForm with POST data
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            # Save the new user
            user = user_form.save()
            form.instance.user = user  # Link the new User to the Profile

            return super().form_valid(form)
        else:
            # If user_form is invalid, re-render the page with errors
            return self.form_invalid(form)

    def form_invalid(self, form):
        # If the profile form is invalid, render both forms with errors
        user_form = UserCreationForm(self.request.POST)
        context = self.get_context_data(form=form, user_form=user_form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy("show_profile", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        # Pass both forms to the template context
        context = super().get_context_data(**kwargs)
        if "user_form" not in context:
            context["user_form"] = UserCreationForm()
        return context


class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def form_valid(self, form):
        # Save the new StatusMessage
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        sm = form.save(commit=False)
        sm.profile = profile
        sm = form.save()

        # Handle file uploads
        files = self.request.FILES.getlist("files")
        for f in files:
            Image.objects.create(image_file=f, status_message=sm)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("show_profile", kwargs={"pk": self.kwargs["pk"]})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "mini_fb/update_profile_form.html"
    fields = [
        "first_name",
        "last_name",
        "city",
        "email",
        "profile_image_url",
    ]  # Specify fields for updating

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"

    def get_success_url(self):
        profile_id = self.object.profile.pk
        return reverse_lazy("show_profile", kwargs={"pk": profile_id})


class CreateFriendView(View):
    def get(self, request, other_pk):
        # Get the profile of the logged-in user
        user_profile = get_object_or_404(Profile, user=request.user)

        # Get the profile of the user to be added as a friend
        friend_profile = get_object_or_404(Profile, pk=other_pk)

        # Add friend if not already friends
        user_profile.add_friend(friend_profile)

        # Redirect back to the friend suggestions page or wherever appropriate
        return redirect("friend_suggestions")


class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"

    def get_object(self, queryset=None):
        # Get the Profile associated with the logged-in user
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        # Add friend suggestions to the context
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["friend_suggestions"] = profile.get_friend_suggestions()
        return context


class ShowNewsFeedView(DetailView):
    template_name = "mini_fb/news_feed.html"
    context_object_name = "news_feed"

    def get_object(self, queryset=None):
        # Retrieve the Profile associated with the logged-in user
        return Profile.objects.get(user=self.request.user)

    def get_queryset(self):
        # Use the get_news_feed method to get the news feed for the user's profile
        user_profile = self.get_object()
        return user_profile.get_news_feed()
