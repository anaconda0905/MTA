import math
import datetime
from datetime import datetime as mydatetime
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator

from markdown import markdown


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):

    feeling = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    bus_no = models.CharField(max_length=100)
    incident_date = models.DateField(default=datetime.date.today)
    incident_time = models.TimeField(default=(mydatetime.now()))
    quick_review = models.CharField(max_length=100)
    route_no = models.CharField(max_length=100)
    route_name = models.CharField(max_length=100)
    bus_operator = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    audit = models.CharField(max_length=255, default="off", blank=True, null=True)
    location = models.PointField()
    # file = models.FileField(upload_to="files/%Y/%m/%d")
    # mulfile = models.FileField(upload_to='mediadata/')
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')
    views = models.PositiveIntegerField(default=0)
    upvote = models.PositiveIntegerField(default=0)
    downvote = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]

class MFile(models.Model):
    board = models.ForeignKey(Board, related_name='files')
    starter = models.ForeignKey(User, related_name='files')
    topic = models.ForeignKey(Topic, related_name='files')
    afile = models.FileField(upload_to="files/%Y/%m/%d", default="/static/img/map-1.png")

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

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
