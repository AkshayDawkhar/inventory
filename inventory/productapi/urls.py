from django.contrib import admin
from django.urls import path,include
from productapi import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.productlist)
]
