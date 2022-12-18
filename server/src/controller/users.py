import json
import bcrypt
import os
import random
import datetime
from flask import request
from bson import json_util
from src.model.user import UserModel
from src.model.activity import ActivityModel
from src.services.mail import mailService

class UserController:
    __model = None
    __body = None

    def __init__(self) -> None:
        self.__model = UserModel()
        self.__body = request.json
    
    def index(self):
        data = self.__model.index()
        return {"message": "Hello", "data": {"users": json.loads(json_util.dumps(data))}}
    
    def create(self):
        user = self.__model.get_single(self.__body['email'])
        if user is not None:
            return {"message": "Email already exists", "data": None}
        salt = bytes(os.getenv("SALT"), 'utf-8')
        self.__body['password'] = bcrypt.hashpw(bytes(self.__body.get('password', '12345678'), 'utf-8'), salt)
        self.__body['verification_otp'] = random.randint(1000,9999)
        data = self.__model.create(self.__body)

        mailService.messageBody("OTP Verification", self.__body['email'], f"OTP: {self.__body['verification_otp']}").send()

        return {"message": "Hello", "data": {"inserted_id": json.loads(json_util.dumps(data))}}
    
    def login(self):
        user = self.__model.get_single(self.__body['email'])
        if user is None:
            return {"message": "Email is not registered", "data": None}
        elif user.get('verification_otp', None):
            return {"message": "Email is not verified", "data": None}
        elif self.__body.get("request_time", None) is None:
            return {"message": "Time is not present", "data": None}

        filter_data = {
            "activity": "login",
            "ref_id": user["_id"],
            "logout_time": {"$exists": False}
        }

        update_date = {
            "$set": {
                "logout_time": datetime.datetime.now()
            }
        }

        ActivityModel().update(filter_data, update_date)

        activity_data = {
            "activity": "login",
            "ref_id": user["_id"],
            "login_time": datetime.datetime.now(),
            "requested_time": self.__body["request_time"]
        }

        ActivityModel().create(activity_data)

        if  self.__body.get('password', None) is not None and bcrypt.checkpw(bytes(self.__body.get('password'), 'utf-8'), user.get('password')):
            return {"message": "Hello", "data": {"inserted_id": json.loads(json_util.dumps(user))}}
        else:
            return {"message": "Password mismatch", "data": None}
    
    def logout(self):
        user = self.__model.get_single(self.__body['email'])
        if user is None:
            return {"message": "Email is not registered", "data": None}

        filter_data = {
            "activity": "login",
            "ref_id": user["_id"]
        }
        
        activity_data = {
            "$set": {
                "logout_time": datetime.datetime.now()
            }
        }

        ActivityModel().update(filter_data, activity_data)
        return {"message": "Logout Successful", "data": True}
    
    def verify(self):
        user = self.__model.get_single(self.__body['email'])

        if user.get('verification_otp', None) is None:
            return {"message": "No verification is pending", "data": None}
        
        if user.get('verification_otp') != self.__body['otp']:
            return {"message": "OTP mismatch", "data": None}

        self.__model.revoke_otp(user.get('email'))

        return {"message": "OTP verified", "data": True}

    def forget_password(self):
        user = self.__model.get_single(self.__body['email'])
        if user is None:
            return {"message": "Email is not registered", "data": None}
        
        otp = random.randint(1000,9999)

        query = {
            "email": self.__body['email']
        }
        
        data = {
            "$set": {
                "verification_otp": otp
            }
        }

        mailService.messageBody("OTP Verification", self.__body['email'], f"OTP: {otp}").send()

        self.__model.update(query, data)
        return {"message": "Email sent", "data": otp}
    
    def reset_password(self):
        user = self.__model.get_single(self.__body['email'])
        if user.get('verification_otp', None) is None:
            return {"message": "No verification is pending", "data": None}
        if user.get('verification_otp') != self.__body['otp']:
            return {"message": "OTP mismatch", "data": None}
        self.__model.revoke_otp(user.get('email'))

        salt = bytes(os.getenv("SALT"), 'utf-8')
        query = {
            "email": self.__body['email']
        }
        data = {
            "$set": {
                "password": bcrypt.hashpw(bytes(self.__body.get('password', '12345678'), 'utf-8'), salt)
            }
        }
        self.__model.update(query, data)
        return {"message": "Password changed", "data": True}
    
    def otp(self, email):
        user = self.__model.get_single(email)
        if user is None:
            return {"message": "Email invalid", "data": None}
        if user.get('verification_otp', None) is None:
            return {"message": "No verification is pending", "data": None}
        
        return user['verification_otp']