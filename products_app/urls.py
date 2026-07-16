from django.urls import path
from . import views 



urlpatterns = [
    path('',views.products_app_view, name='products'),
    path('detail/<id1>/<slug>/',views.product_detail_view,name= 'id_slug_to_product'),
    path('detail/<id1>/',views.product_detail_view,name= 'id_to_product'),
]

