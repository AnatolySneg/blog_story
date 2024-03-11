from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    title_image = models.ImageField(null=True, blank=True, upload_to="images/")
    text = models.TextField(max_length=3000)
    created_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(default=timezone.now)

    @staticmethod
    def edit():
        return timezone.now()

    def __str__(self):
        return self.title
