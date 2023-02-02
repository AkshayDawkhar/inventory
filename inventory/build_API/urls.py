from django.urls import path
from . import views

urlpatterns = [
    path('', views.BuildProducts.as_view(), name='get_builds'),
    path('<uuid:pid>', views.BuildProduct.as_view(), name='build_product'),
    path('edit/<uuid:pid>', views.EditBuildProduct.as_view(), name='get_build'),
    path('required/<uuid:pid>', views.RequiredItem.as_view(), name='get_required_item'),
    path('required/', views.RequiredItems.as_view(), name='get_required_items'),
    path('needed/<uuid:rid>', views.RequiredFor.as_view(), name='get_row_needed'),
    path('edit/stock/<uuid:pid>', views.EditStock.as_view(), name='edit_stock'),
    path('stock/<uuid:pid>', views.Stock.as_view(), name='stock'),
    path('maxbuild/<uuid:pid>', views.GetMax.as_view(), name='get_max')
]
