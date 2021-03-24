from django.urls import path
from . import views
from .views import UserList, UserCreate, UserUpdate
from .views import RolList, RolCreate, RolUpdate, RolDelete

urlpatterns = [
    path('users/', UserList.as_view(), name="user_list"),
    path('users/create', UserCreate.as_view(), name="user_create"),   
    path('users/update/<int:pk>/', UserUpdate.as_view(), name="user_update"),
    path('rols/', RolList.as_view(), name="rol_list"),
    path('rols/create', RolCreate.as_view(), name="rol_create"),   
    path('rols/update/<int:pk>/', RolUpdate.as_view(), name="rol_update"),
    path('rols/delete/<int:pk>/', RolDelete.as_view(), name="rol_delete"),
]