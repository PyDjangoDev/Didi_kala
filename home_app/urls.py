from django.urls import path
from . import views 

urlpatterns = [
    path('',views.home_app_view, name='home'),
    path('amazing-products/', views.amazing_products_all_view, name='amazing_products_all'),
]

