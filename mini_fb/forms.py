from django import forms
from .models import Profile
from .models import StatusMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "city", "email", "profile_image_url"]


class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ["message"]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["city", "email", "profile_image_url"]
