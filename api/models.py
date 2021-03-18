from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Rol(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.name

class User(AbstractUser):
    pass
    rol = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username

