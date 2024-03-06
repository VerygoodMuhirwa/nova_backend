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
from drf_yasg.utils import swagger_auto_schema


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
@api_view(["GET"])
@swagger_auto_schema(tags=[' User APIs'])
def authenticateToken(request):
    response=Response()
    token = request.COOKIES.get('jwt')
    if not token:
        response.data="No token found"       
    try:
        payload = jwt.decode(token, str(os.getenv("JWT_SECRET")), algorithms=['HS256'])
        user_id = payload['id']   
        user_exist=user_collection.find_one({"_id": ObjectId(user_id)})        
        print(user_exist)
        if(user_exist):
            user={
                           "id":user_id,
                           "email":user_exist.get('email'),
                           "username":user_exist.get('username')
                           }
            return user;
        else:
            return Response("Invalid token", status= 401);
    except Exception as e:
        print(e)
        response.status_code(500)
        response.data("Internal server error")
        return response
        
        
        
        


# this shows how we can simply authenticate the person using the custom class that we have created ours selves
@csrf_protect
@swagger_auto_schema(tags=[' User APIs'])
def example_api(request):
    auth_middleware = authenticateToken()
    user = auth_middleware.authenticate(request)
    
    if user:
        return Response({'message': 'Authenticated successfully'})
    else:
        return Response({'error': 'Authentication failed'}, status=401)
        
