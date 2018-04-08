from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    department=models.CharField(max_length=500, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Patient(models.Model):
    patient_number=models.CharField(max_length=500,blank=True)
    firstname=models.CharField(max_length=500, blank=True)
    lastname=models.CharField(max_length=500, blank=True)
    birth_date=models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=1,blank=True)
    address=models.CharField(max_length=500, blank=True)
    contact=models.CharField(max_length=500,blank=True)
    date_created=models.DateField(auto_now=True)

class Diasese(models.Model):
    name=models.CharField(max_length=400, blank=True)
    date_created=models.DateField(auto_now=True)
    drug=models.ForeignKey('Drug', on_delete=models.CASCADE)

class Drug(models.Model):
    name=models.CharField(max_length=500, blank=True)
    date_created=models.DateField(auto_now=True)



