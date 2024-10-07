from django.http import JsonResponse
from rest_framework.decorators import api_view
from nova_backend.db_connection import MongoConnection  # Import the MongoDB connection class
from user.models import User
from .models import VerificationCode
from django.views.decorators.csrf import csrf_protect
@csrf_protect
@api_view(["POST"])
def save_verification_code(request):
    email = request.data.get('email')
    code = request.data.get('code')

    user = User.find_by_email(email)
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Connect to the 'verification_codes' collection
    connection = MongoConnection()
    collection = connection.get_collection('verification_codes')

    # Check if a verification code already exists for this email
    existing_code = collection.find_one({'email': email})

    if existing_code:
        # Update the existing verification code
        collection.update_one({'email': email}, {'$set': {'code': code}})
    else:
        # Insert a new verification code
        verification_data = {
            'email': email,
            'code': code
        }
        collection.insert_one(verification_data)

    return JsonResponse({'message': 'Code saved successfully'}, status=200)

@csrf_protect
@api_view(["POST"])
def verify_verification_code(request):
    email = request.data.get('email')
    code = int(request.data.get('code'))  # Ensure the code is an integer
    print(code, email)

    # Find the user by email in MongoDB (replace Django ORM query)
    user = User.find_by_email(email)
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Connect to the 'verification_codes' collection
    connection = MongoConnection()
    collection = connection.get_collection('verification_codes')

    verification_code = collection.find_one({'email': email, 'code': code})

    if not verification_code:
        return JsonResponse({'error': 'Invalid code'}, status=400)

    return JsonResponse({'message': 'Code verified successfully'}, status=200)
