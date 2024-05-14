from django.urls import path
from . import views

urlpatterns = [
    path('store_verification_code', views.save_verification_code),
    path("verify_code", views.verify_verification_code)
]

