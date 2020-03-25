from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
import datetime

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullname = models.CharField(max_length=30, blank=True)
    nric = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(default=datetime.date.today, blank=True, null=True)
    phone = PhoneNumberField(blank=True, help_text='Contact phone number')
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)


class Survey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="survey")
    question = models.CharField(max_length=3000, blank=True, null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
