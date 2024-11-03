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


class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_success_url(self):
        return reverse_lazy("show_profile", kwargs={"pk": self.object.pk})


class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"

    def get_success_url(self):
        profile_id = self.object.profile.pk
        return reverse_lazy("show_profile", kwargs={"pk": profile_id})


class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=kwargs["pk"])
        other_profile = Profile.objects.get(pk=kwargs["other_pk"])
        profile.add_friend(other_profile)
        return redirect("show_profile", pk=profile.pk)


class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"


class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
