from django.urls import path
from . import views

urlpatterns = [
    path('generate-confirmation-code', views.GenerateConfirmationCode.as_view(), name='generate-confirmation-code'),
    path("verifyConfirmationCode", views.VerifyConfirmationCode.as_view(), name="verifyConfirmationCode")
]
