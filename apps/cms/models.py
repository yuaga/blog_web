from django.db import models
from apps.login.models import User


class NewsCategory(models.Model):
    name = models.CharField(max_length=6)


class News(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=120)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True)
    thumbnail = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']
