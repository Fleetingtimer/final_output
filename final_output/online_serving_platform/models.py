from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_post_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)


class News(models.Model):
    NEWS_TYPES = (
        ('S', 'Study'),
        ('N', 'Notation'),
        ('A', 'Activity'),
    )
    title = models.CharField(max_length=30, unique=True)
    content = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30, blank=True, default="administrator")
    type = models.CharField(max_length=2, choices=NEWS_TYPES)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    # @classmethod
    # def get_latest_six_news(self):
    #     return self.objects.order_by('-created_at')[:6]

