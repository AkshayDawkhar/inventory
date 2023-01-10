from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.ProductList.as_view()),
    path('<uuid:pid>', views.GetProduct.as_view())
]
