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

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.pk})
    
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        # Save the new StatusMessage
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        sm = form.save(commit=False)
        sm.profile = profile 
        sm = form.save()

        # Handle file uploads
        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(image_file=f, status_message=sm)
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.kwargs['pk']})
    
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.pk})

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    
    def get_success_url(self):
        profile_id = self.object.profile.pk
        return reverse_lazy('show_profile', kwargs={'pk': profile_id})