from django.urls import path 
from .views import *


urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(), name='register'),
    path('otp/',OtpView.as_view(),name='otp'),
    path('logout/',log_out,name='logout')
]

