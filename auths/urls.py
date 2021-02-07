from django.conf.urls import url
from . import views
from django.urls import path
from ih_pharmacie.views import home

urlpatterns = [
    path('', home, name="home"),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('userparams/', views.user_params, name='userparams'),
]

