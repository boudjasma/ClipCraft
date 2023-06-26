from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    picture = models.ImageField(default="media/static/assets/placeholder.jpg", upload_to='media/images/profile_picture/')
    description = models.CharField(max_length=1000)
    videos = models.ManyToManyField('Video')

    def __str__(self):
        return self.user.username

class Video(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=3000)
    avatar = models.ImageField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    evaluation = models.IntegerField(blank=True, null=True, default=5)
    url = models.URLField(null=False)

    def __str__(self):
        return self.title

class VideoFeedback(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    mark = models.IntegerField(default=5)

    def __str__(self):
        return self.video.title