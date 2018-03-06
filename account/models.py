from __future__ import unicode_literals

from django.db import models
from home.models import User

class Volunteer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_humanaid',
    )
    name = models.CharField(max_length=70)
    usertype = models.CharField(max_length=50)
    humanaid = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    loyalto = models.CharField(max_length=70,default='nil')

    def __str__(self):
        return self.name

class Accomadation(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_capacity',
    )
    name = models.CharField(max_length=70)
    usertype = models.CharField(max_length=50)
    capacity = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    loyalto = models.CharField(max_length=70,default='nil')

    def __str__(self):
        return self.name

class Pronearea(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_population',
    )
    name = models.CharField(max_length=70)
    usertype = models.CharField(max_length=50)
    population = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    loyalto = models.CharField(max_length=70,default='nil')

    def __str__(self):
        return self.name

class Hospital(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_occupy',
    )
    name = models.CharField(max_length=70)
    usertype = models.CharField(max_length=50)
    canoccupy = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    loyalto = models.CharField(max_length=70,default='nil')

    def __str__(self):
        return self.name
