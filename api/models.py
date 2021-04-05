from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
# Create your models here.

class Permiso(models.Model):
    # PERMISOS = (
    #     ('21', 'add_rol'),
    #     ('22', 'changue_rol'),
    #     ('23', 'delete_rol'),
    #     ('25', 'add_user'),
    #     ('26', 'changue_user'),
    #     ('27', 'delete_user'),
    # )
    name = models.CharField(max_length=20, null=False, blank=False)

class Rol(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    permisos = models.ManyToManyField(Permiso, blank=True)
    def __str__(self):
        return self.name

class User(AbstractUser):
    rol = models.CharField(max_length=20, blank=True)
    #rol = models.ForeignKey(Rol, null=True, on_delete=models.SET_NULL)
    user_verified = models.BooleanField(null = True)
    verified_code = models.CharField(max_length=40, null = True)

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username
 