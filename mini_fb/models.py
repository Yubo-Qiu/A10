from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        return self.statusmessage_set.all().order_by("-timestamp")

    def get_friends(self):
        friends = Friend.objects.filter(
            models.Q(profile1=self) | models.Q(profile2=self)
        )
        return [f.profile2 if f.profile1 == self else f.profile1 for f in friends]

    def add_friend(self, other):
        if (
            self != other
            and not Friend.objects.filter(
                models.Q(profile1=self, profile2=other)
                | models.Q(profile1=other, profile2=self)
            ).exists()
        ):
            Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        current_friends = self.get_friends()
        return Profile.objects.exclude(
            pk__in=[self.pk] + [friend.pk for friend in current_friends]
        )

    def get_news_feed(self):
        friends = self.get_friends()
        news_feed = StatusMessage.objects.filter(profile__in=[self] + friends).order_by(
            "-timestamp"
        )
        print(
            "News Feed for:",
            self,
            "includes messages from profiles:",
            [p.first_name for p in [self] + friends],
        )
        print("Number of status messages in feed:", news_feed.count())
        return news_feed


class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.message} (posted by {self.profile.first_name} at {self.timestamp})"
        )

    def get_images(self):
        return self.image_set.all()


class Image(models.Model):
    image_file = models.ImageField(
        upload_to="images/"
    )  # Store images in a directory called 'images/'
    status_message = models.ForeignKey(
        StatusMessage, on_delete=models.CASCADE
    )  # Foreign key to StatusMessage
    timestamp = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set timestamp when an image is added

    def __str__(self):
        return f"Image for {self.status_message} uploaded on {self.timestamp}"


class Friend(models.Model):
    profile1 = models.ForeignKey(
        Profile, related_name="profile1", on_delete=models.CASCADE
    )
    profile2 = models.ForeignKey(
        Profile, related_name="profile2", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
