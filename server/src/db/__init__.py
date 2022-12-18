import os
from pymongo import MongoClient

class DB:
    __instance = None
    __client = None

    def __new__(cls):
        if DB.__instance is None:
            DB.__instance = super(DB, cls).__new__(cls)
        return DB.__instance
    
    def connect(self):
        if self.__client is None:
            connection_str: str = os.getenv("MONGO_URL")
            self.__client = MongoClient(connection_str)
    
    def db(self):
        return self.__client.get_default_database()