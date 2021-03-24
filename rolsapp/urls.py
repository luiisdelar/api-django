from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.rols, name='rols'),
    path('create/', views.createRol, name='create-rol'),
    path('edit/<int:pk>', views.editRol, name='edit-rol'),
    path('delete/<int:pk>', views.deleteRol, name='delete-rol'),
    path('permissions/<int:pk>', views.permissionsRol, name='permissions-rol'),
]