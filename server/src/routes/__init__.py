import json
from flask import Flask
from bson import json_util
from src.controller.users import UserController

class Route:
    __app: Flask

    def __init__(self, app: Flask) -> None:
        self.__app = app
    
    def load(self):
        @self.__app.route('/')
        def index():
            return UserController().index()
        
        @self.__app.route('/register', methods=['POST'])
        def register():
            return UserController().create()
        
        @self.__app.route('/login', methods=['POST'])
        def login():
            return UserController().login()
        
        @self.__app.route('/verify', methods=['POST'])
        def verify_otp():
            return UserController().verify()
        
        @self.__app.route('/forget_password', methods=['POST'])
        def forget_password():
            return UserController().forget_password()

        @self.__app.route('/reset_password', methods=['POST'])
        def reset_password():
            return UserController().reset_password()
        
        @self.__app.route('/otp/<email>')
        def otp(email):
            return UserController().otp(email)
            
