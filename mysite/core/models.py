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

    def age(self):
        import datetime
        return int((datetime.date.today() - self.birth_date).days / 365.25)

class PatientRecords(models.Model):
    chest_pain=models.IntegerField(blank=True, null=True)
    trestbps=models.IntegerField(blank=True, null=True)
    chol=models.IntegerField(blank=True, null=True)
    fbs=models.IntegerField(blank=True, null=True)
    restEcg=models.IntegerField(blank=True, null=True)
    thalach=models.IntegerField(blank=True, null=True)
    exang=models.IntegerField(blank=True, null=True)
    oldPeak = models.IntegerField(blank=True, null=True)
    slope = models.IntegerField(blank=True, null=True)
    ca = models.IntegerField(blank=True, null=True)
    thal = models.IntegerField(blank=True, null=True)
    date_created=models.DateField(auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)

class Prescribe(models.Model):
    patient=models.ForeignKey('Patient', on_delete=models.CASCADE)
    drug = models.ForeignKey('Drug', on_delete=models.CASCADE)
    date_created=models.DateField(auto_now=True)



class Drug(models.Model):
    name=models.CharField(max_length=500, blank=True)
    date_created=models.DateField(auto_now=True)
    type=models.CharField(max_length=200, blank=True)
    formulation=models.CharField(max_length=200,blank=True)



