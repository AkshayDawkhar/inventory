from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.accounts.as_view()),
    path('<str:username>', views.account.as_view()),
    path('login/', views.WorkerLogin.as_view()),
    path('username/', views.WorkerUsername.as_view()),
    path('admin/', views.admins.as_view()),
    path('admin/<str:username>', views.admin.as_view()),
    path('admin/login/', views.AdminLogin.as_view()),
]
