from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.users), name='users'),
    path('profile/', login_required(views.profile), name='profile'),
    path('create/', login_required(views.createUser), name='create-user'),
    path('edit/<int:pk>', login_required(views.editUser), name='edit-user'),
    path('delete/<int:pk>', login_required(views.deleteUser), name='delete-user'),
    path('register/', views.registerUser, name='register'),
    path('verified-email/', login_required(views.verifiedEmail), name='verfiedemail'),
    path('forgot-password/', views.forgotPassword, name='forgotPassword'),
    path('permission-denied/', views.permission_denied, name='permission_denied'),
]