from django.db import models

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.message} (posted by {self.profile.first_name} at {self.timestamp})"
    
    def get_images(self):
        return self.image_set.all()

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')  # Store images in a directory called 'images/'
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)  # Foreign key to StatusMessage
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set timestamp when an image is added

    def __str__(self):
        return f"Image for {self.status_message} uploaded on {self.timestamp}"