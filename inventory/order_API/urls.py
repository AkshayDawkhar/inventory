from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Orders.as_view()),
    path('edit/<uuid:pid>', views.EditOrder.as_view()),
    path('<uuid:pid>', views.Order.as_view())
]
