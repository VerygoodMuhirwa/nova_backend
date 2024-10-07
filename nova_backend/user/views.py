import os
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from bson import ObjectId
import jwt
from django.core.serializers.json import DjangoJSONEncoder
from nova_backend.db_connection import MongoConnection
from pymongo.errors import DuplicateKeyError


class MongoEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


def authenticate_user(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"message": "Authentication credentials were not provided"}, status=401)

        token = auth_header.split(' ')[1]
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

    hashed_password = make_password(password, hasher="bcrypt")

    connection = MongoConnection()
    collection = connection.get_collection('users')

    new_user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "photo": "https://icon-library.com/images/anonymous-avatar-icon/anonymous-avatar-icon-25.jpg",
        "phoneNumber": ""
    }

    try:
        # Try to insert the new user (check for duplicate emails)
        collection.insert_one(new_user)
    except DuplicateKeyError:
        return Response({"message": "User with that email already exists"}, status=409)

    # Serialize user info without password
    serialized_user = {
        "id": str(new_user["_id"]),
        "username": new_user["username"],
        "email": new_user["email"]
    }

    return Response({"message": "User created successfully", "user": serialized_user}, status=200)


@csrf_protect
@api_view(["POST"])
def loginUser(request):
    email = request.data.get('email')
    password = request.data.get('password')

    connection = MongoConnection()
    collection = connection.get_collection('users')

    # Find user by email
    user = collection.find_one({"email": email})
    if not user:
        return Response({"message": "Invalid email or password"}, status=401)

    if check_password(password, user['password']):
        payload = {"id": str(user["_id"])}
        token = jwt.encode(payload, str(os.getenv('JWT_SECRET')), algorithm='HS256')
        user_data = {
            "_id": str(user["_id"]),
            "names": user["username"],
            "email": user["email"],
            "profilePhoto": user.get("photo", "")
        }
        response_data = {"token": token, "message": "Logged in successfully", "user": user_data}
        return Response(data=response_data, status=200)
    else:
        return Response({"message": "Invalid email or password"}, status=401)


@csrf_protect
@api_view(["PUT"])
@authenticate_user
def updateProfile(request):
    user_id = request.user_id  # Access the user ID from the request
    request_data = request.data
    email = request_data.get("email")
    username = request_data.get("username")
    phoneNumber = request_data.get("phoneNumber")
    newPassword = request_data.get("newPassword")
    oldPassword = request_data.get("oldPassword")
    photo = request_data.get("photo")

    connection = MongoConnection()
    collection = connection.get_collection('users')

    user = collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return Response({"message": "User not found"}, status=404)

    if check_password(oldPassword, user["password"]):
        saved_password = make_password(newPassword, hasher="bcrypt")
        update_data = {
            "username": username,
            "phoneNumber": phoneNumber,
            "email": email,
            "photo": photo,
            "password": saved_password
        }
        collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

        serialized_user = {
            "id": str(user["_id"]),
            "username": username,
            "email": email,
            "phone_number": phoneNumber,
            "photo": photo
        }
        return Response({"message": "Profile updated successfully", "user": serialized_user})
    else:
        return Response({"message": "Invalid password"}, status=401)


@csrf_protect
@api_view(["PUT"])
@authenticate_user
def updatePassword(request):
    user_id = request.user_id
    request_data = request.data
    email = request_data.get("email")
    new_password = request_data.get("newPassword")

    connection = MongoConnection()
    collection = connection.get_collection('users')

    user = collection.find_one({"_id": ObjectId(user_id), "email": email})

    if not user:
        return Response({"message": "User not found"}, status=404)

    hashed_password = make_password(new_password, hasher="bcrypt")
    collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"password": hashed_password}})

    return Response({"message": "Password updated successfully"})
