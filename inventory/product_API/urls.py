from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.ProductList.as_view(), name='get_products'),
    path('<uuid:pid>', views.Product.as_view(), name='get_product'),
    path('trash/', views.Trashes.as_view(), name='get_trashes'),
    path('trash/<uuid:pid>', views.Trash.as_view(), name='get_trash')
]
