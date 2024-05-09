import base64
import os
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from bson import ObjectId
from django.core.serializers.json import DjangoJSONEncoder
from .models import User
import jwt


class MongoEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def authenticate_user(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response({"message": "Authentication credentials were not provided"}, status=401)

        try:
            payload = jwt.decode(token, str(os.getenv('JWT_SECRET')), algorithms=['HS256'])
            user_id = payload['id']
            request.user_id = user_id
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid token"}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper


@csrf_protect
@api_view(["POST"])
def registerUser(request):
    request_data = request.data
    username = request_data["names"]
    email = request_data["email"]
    password = request_data["password"]
    
    if User.objects.filter(email=email).exists():
        return Response({"message": "User with that email already exists"}, status=409)
    
    hashed_password = make_password(password, hasher="bcrypt")
    new_user = User(username=username, email=email, password=hashed_password)
    new_user.save()

    serialized_user= {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }
    
    return Response({"message": "User created successfully", "user":serialized_user}, status=200)

@csrf_protect
@api_view(["POST"])
def loginUser(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()
    print(user)
    if not user:
        return Response({"message": "Invalid email or password"}, status=401)
    
    if check_password(password, user.password):
        payload = {"id": str(user.id)}
        token = jwt.encode(payload, str(os.getenv('JWT_SECRET')), algorithm='HS256')
        user_data = {"_id": str(user.id), "names": user.username, "email": user.email,"profilePhoto":user.photo}
        response_data = {"token": token, "message": "Logged in successfully", "user": user_data}
        response = Response(data=response_data, status=200)
        response.set_cookie(key='jwt', value=token, httponly=True)
        return response
    else:
        return Response({"message": "Invalid email or password"}, status=401)

@csrf_protect
@api_view(["PUT"])
@authenticate_user
def updateProfile(request):  # Remove user_id as a parameter
    user_id = request.user_id  # Access the user ID from the request
    request_data = request.data
    email = request_data.get("email")
    username = request_data.get("username")
    phoneNumber = request_data.get("phoneNumber")
    newPassword = request_data.get("newPassword")
    oldPassword = request_data.get("oldPassword")
    photo = request_data.get("photo")

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
    if check_password(oldPassword, user.password):
        saved_password = make_password(newPassword, hasher="bcrypt")
        user.username = username
        user.phoneNumber = phoneNumber
        user.email = email
        user.photo = photo
        user.password = saved_password
        user.save()

        serialized_user = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phoneNumber,
            "photo": user.photo
        }
        return Response({"message": "Profile updated successfully", "user": serialized_user})
    else:
        return Response({"message": "Invalid email or password"}, status=401)