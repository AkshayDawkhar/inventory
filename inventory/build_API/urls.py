from django.urls import path
from . import views

urlpatterns = [
    path('', views.BuildProducts.as_view(), name='get_builds'),
    path('<uuid:pid>', views.BuildProduct.as_view(), name='get_build'),
    path('required/<uuid:pid>', views.RequiredItem.as_view(), name='get_required_items'),
]
