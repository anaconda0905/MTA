from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Board, Post, Topic, MFile, Comment, Vote

admin.site.register(Board)
admin.site.register(Post)
admin.site.register(MFile)
admin.site.register(Comment)
admin.site.register(Vote)
@admin.register(Topic)
class TopicAdmin(OSMGeoAdmin):
    pass

