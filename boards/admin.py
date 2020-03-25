from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Board, Post, Topic, MFile

admin.site.register(Board)
admin.site.register(Post)
admin.site.register(MFile)

@admin.register(Topic)
class TopicAdmin(OSMGeoAdmin):
    pass

