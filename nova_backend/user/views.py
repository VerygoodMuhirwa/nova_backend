import datetime
import os
from django.shortcuts import render
from django.http import HttpResponse
from dotenv import  load_dotenv
from django.views.decorators.csrf import csrf_protect
import jwt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from bson import ObjectId
import json
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.core.serializers.json import DjangoJSONEncoder
from .models import user_collection
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import BlacklistMixin
import jwt
from django.conf import settings

blacklisted_tokens = set()
load_dotenv()
class MongoEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)
@csrf_protect
@api_view(["POST"])
def registerUser(request):
    from .models import user_collection  
    request_data = request.data
    print(request_data)
    username = request_data["names"]
    email = request_data["email"]
    password = request_data["password"]
    user_exists = user_collection.find_one({"email": email})
    response = Response()
    if user_exists:
        response.status_code= 409;
        response.data= {"message":"User with that email already exists "}
    else:
        hashed_password = make_password(password, hasher="bcrypt")
        new_user = {
            "username": username,
            "email": email,
            "password": hashed_password
        }
        serialized_user = json.dumps(new_user, cls=MongoEncoder)
        new_user = json.loads(serialized_user)
        user_collection.insert_one(new_user)
        response.status_code =200
        response.data= {
            "message":"User created successfully",
            }
    return response;



@csrf_protect
@api_view(["POST"])
def loginUser(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user_exists  = user_collection.find_one({"email": email});
    if not user_exists:
        return Response({"message":"Invalid email or password"}, status= 401);
    else:
        storedPassword = user_exists.get("password")
        isAuthenticated = check_password(password, storedPassword)
        if(isAuthenticated) :
               payload = {"id": str(user_exists.get("_id"))}
               token = jwt.encode(payload, str(os.getenv('JWT_SECRET')) , algorithm='HS256')
               user= {
                   "_id":str(user_exists.get("_id")),
                   "names":str(user_exists.get("username")),
                   "email":str(user_exists.get("email"))
               }
               response = Response(data={"token": token, "message":"Logged in successfully","user": user }, status=200)
               response.set_cookie(key='jwt', value=token, httponly=True)
               return response
        else:
            return Response({"message":"Invalid email or password"}, status= 401);
    

    
@csrf_protect
@api_view(["POST"])
def logout_user(request):
    token = request.COOKIES.get('jwt')  
    
    if not token:
        return Response({'error': 'No token found in the cookie'}, status=400)
    if is_valid_token(token) and token not in blacklisted_tokens:
        response = Response({'message': 'Logged out successfully'}, status=200)
        response.delete_cookie('jwt')
        blacklisted_tokens.add(token)   
        return response
    else:
        return Response({'error': 'Invalid or blacklisted token'}, status=401)



def is_valid_token(token):
    try:
        decoded_token = jwt.decode(token, str(os.getenv("JWT_SECRET")), algorithms=['HS256'])
        if decoded_token and token in blacklisted_tokens:
            return False  
        else:
            return True 
    except jwt.ExpiredSignatureError:
        return False 
    except jwt.InvalidTokenError:
        return False 