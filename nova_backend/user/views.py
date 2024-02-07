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
    from .models import user_collection  
    request_data = request.data
    email = request_data.get('email')
    password = request_data.get('password')
    user_exists = user_collection.find_one({"email": email})
    if not user_exists:
        return Response({"message": "Invalid email or password"}, status=404)
    else:
        stored_password = user_exists.get("password")
        if check_password(password, stored_password):
            response=Response()
            if user_exists is not None:
                user_id = user_exists.get("_id")            
                payload = {
               "id": str(user_id),
                }
            
                print(os.getenv("JWT_SECRET"))
                token=jwt.encode(payload,str(os.getenv('JWT_SECRET')),algorithm='HS256')
                if user_exists:
                    response.data = token
                    
                    response.set_cookie(key='jwt', value=token, httponly=True)
                else:
                    response.status_code = 404
                    response.data="Login failed"                
                return response               
            else:
                return Response({"message": "Invalid email or password"}, status=401)
        else:
            return Response({"message": "Invalid email or password"}, status=401)
        
        
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
            response.status_code=200
            response.data={"id":user_id,
                           "email":user_exist.get('email'),
                           "username":user_exist.get('username')}
        else:
            response.data="User does not exist"
        
        return response 
    except Exception as e:
        print(e)
        response.status_code(500)
        response.data("Something went wrong")
        return response
        
        
        
