from __future__ import unicode_literals

from django.db import models
from home.models import User


class Food(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_food',
    )
    packet = models.IntegerField(null=True)


class Water(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_water',
    )
    quantity = models.IntegerField(null=True)


class Firstaid(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_firstaid',
    )
    kit = models.IntegerField(null=True)


class Rescuetool(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_rescuetool',
    )
    box = models.IntegerField(null=True)


class Machine(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_machine',
    )
    fireengine = models.IntegerField(null=True)
    jcb = models.IntegerField(null=True)
    ambulance = models.IntegerField(null=True)


class TransportGoods(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_transportg',
    )
    capacity = models.IntegerField(null=True)


class TransportHuman(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='updates_transporth',
    )
    capacity = models.IntegerField(null=True)


class Messagebox(models.Model):
    fromaddr = models.CharField(max_length=70)
    toaddr = models.CharField(max_length=70)
    timestamp=models.DateTimeField(auto_now=True)
    topic = models.CharField(max_length=70)
    message= models.CharField(max_length=500)
    parameter=models.CharField(max_length=100,null=True)
    ack = models.BooleanField(default=False)
    nack= models.BooleanField(default=False)