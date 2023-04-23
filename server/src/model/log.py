from datetime import datetime, timedelta
from src.db import DB

class LogModel:
    collection_name = 'logs'
    __collection = None
    __db = None

    def __init__(self) -> None:
        self.__db = DB().db()
        self.__collection = self.__db[self.collection_name]

    def create(self, data):
        self.__collection.insert_one(data)