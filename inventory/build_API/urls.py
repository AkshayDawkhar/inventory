from django.urls import path
from . import views

urlpatterns = [
    path('', views.BuildProducts.as_view(), name='get_builds'),
]
