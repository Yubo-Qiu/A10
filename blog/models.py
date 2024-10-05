from django.db import models

# Create your models here.
from django.db import models

class Article(models.Model):
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"