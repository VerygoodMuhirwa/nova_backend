

from django.http import JsonResponse
from user.models import User
from .models import VerificationCode
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
@csrf_protect
@api_view(["POST"])
def save_verification_code(request):
    email = request.data.get('email')
    code = request.data.get('code')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    verification_code, created = VerificationCode.objects.get_or_create(email=email)

    if not created:
        verification_code.code = code
        verification_code.save()
    else:
        verification_code.code = code
        verification_code.save()

    return JsonResponse({'message': 'Code saved successfully'}, status=200)



@csrf_protect
@api_view(["POST"])
def verify_verification_code(request):
    email = request.data.get('email')
    code = request.data.get('code')
    print(code, email)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    try:
        verification_code = VerificationCode.objects.get(email=email, code=code)
    except VerificationCode.DoesNotExist:
        return JsonResponse({'error': 'Invalid code'}, status=400)

    return JsonResponse({'message': 'Code verified successfully'}, status=200)