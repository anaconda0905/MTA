from django.contrib import admin
from .models import Profile, Survey
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile, ProfileAdmin)

class SurveyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Survey, SurveyAdmin)