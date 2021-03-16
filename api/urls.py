from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='apiOverview'),
    path('user-list/', views.showAll, name='user-list'),
    path('user-detail/<int:pk>/', views.viewUser, name='view-user'),
    path('user-create/', views.createUser, name='create-user'),
    path('user-update/<int:pk>/', views.updateUser, name='update-user'),
    path('user-delete/<int:pk>/', views.deleteUser, name='delete-user'),
    path('rol-list/', views.showAllRols, name='rol-list'),
    path('rol-detail/<int:pk>/', views.viewRol, name='view-rol'),
    path('rol-create/', views.createRol, name='create-rol'),
    path('rol-update/<int:pk>/', views.updateRol, name='update-rol'),
    path('rol-delete/<int:pk>/', views.deleteRol, name='delete-rol'),
]