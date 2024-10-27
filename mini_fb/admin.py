from django.contrib import admin

# Register your models here.
from .models import Profile

admin.site.register(Profile)

from .models import StatusMessage, Image, Friend

admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)