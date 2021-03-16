from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.users, name='users'),
    path('create/', views.createUser, name='create-user'),
    path('edit/<int:pk>', views.editUser, name='edit-user'),
    path('delete/<int:pk>', views.deleteUser, name='delete-user'),
]