from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50,primary_key=True)
    category = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    location = models.CharField(max_length=70)
    longitude = models.FloatField()
    latitude = models.FloatField()
    email = models.EmailField(max_length=254)
    contact_no =models.CharField(max_length=14)

    def __str__(self):
        return self.username
