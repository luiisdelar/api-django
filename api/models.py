from django.db import models


# Create your models here.

class Rol(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=30, null=False, blank=False, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    password = models.CharField(max_length=101, null=False, blank=False)
    rol = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.username

