from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core import views
from .views import *

urlpatterns = [
    # TESTE dozent, usw. FORM
    path('dozent/', views.dozent, name='dozent'),
    path('kurs/', views.kurs, name='module'),
    path('tutor/', views.tutor, name='tutor'),
    # path('tutorprofile/', views.tutorprofile, name='tutorprofile'),
    path('kursleiter/', views.kursleiter, name='kursleiter'),
    # path('kursleiterprofile/', views.kursleiterprofile, name='kursleiterprofile'),
    path('user/', views.user, name='user'),
    path('profile', views.profile, name='profile'),

    # Ok - Erfolgreich gespeichert
    path('ok/', views.ok, name='ok'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    # set password
    path('' , Home , name="home"),
    path('login/' , login , name="login"),\
    path('register/' , register , name="register"),
    path('set-password/' , setPassword , name="set-password"),
    path('change-password/<token>/' , changePassword , name="change_password"),
    path('logout/' , logout , name="logout"),
]