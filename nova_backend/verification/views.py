from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, VerificationCode
from .serializers import VerificationCodeSerializer
from django.core.mail import send_mail
from django.conf import settings


class GenerateConfirmationCode(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        confirmation_code = generate_confirmation_code()
        verification_code = VerificationCode.objects.create(user=user, code=confirmation_code)

        serializer = VerificationCodeSerializer(verification_code)

        subject = 'Nova Password Reset Confirmation Code'
        message = f'Your Nova reset password confirmation code is: {confirmation_code}. Please use this code to reset your password. Click here to go to the password reset page: http://localhost:3000/verification'
        sender_email = settings.EMAIL_HOST_USER  
        recipient_list = [email]

        send_mail(subject, message, sender_email, recipient_list, fail_silently=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


def generate_confirmation_code():
    import random
    return ''.join(random.choices('0123456789', k=6))


class VerifyConfirmationCode(APIView):
    def post(self, request):
        code = request.data.get('code')  
        try:
            verification_code = VerificationCode.objects.get(code=code)
            print(verification_code)
        except VerificationCode.DoesNotExist:
            return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)

        verification_code_data = verification_code._id

        verification_code.delete() 

        return Response({'message': 'Code verified successfully', 'verification_code_data': verification_code_data}, status=status.HTTP_200_OK)