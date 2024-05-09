from django.urls import path
from . import views
urlpatterns= [
    path("registerUser" , views.registerUser),
    path("loginUser", views.loginUser),
    path("updateProfile", views.updateProfile),
]

