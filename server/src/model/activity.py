from datetime import datetime, timedelta
from src.db import DB

class ActivityModel:
    collection_name = 'activities'
    __collection = None
    __db = None

    def __init__(self) -> None:
        self.__db = DB().db()
        self.__collection = self.__db[self.collection_name]

    def index(self):
        users = list(self.__collection.find())
        return users
    
    def create(self, data):
        new_user_id = self.__collection.insert_one(data).inserted_id
        return new_user_id
    
    def get_single(self, query):
        user = self.__collection.find_one(query)
        return user
    
    def revoke_otp(self, email):
        return self.__collection.update_one({
            "email": email
        }, {
            "$unset": {
                "verification_otp": ""
            }
        })
    
    def update(self, query, data):
        return self.__collection.update_one(query, data)
    
    def get_all_not_logout(self):
        self.__collection.update_many({
            "logout_time": {"$exists": False},
            "last_active": {"$lt": datetime.now() - timedelta(minutes=5)}
        }, {
            "$set": {"logout_time": datetime.now()}
        })
    
    def totalPrayer(self):
        return self.__collection.aggregate([
            {
                "$lookup": {
                    "from": "users",
                    "localField": "ref_id",
                    "foreignField": "_id",
                    "as": "user",
                },
            },
            {
                "$group": {
                    "_id": {"name": {"$first": "$user.name"}, "email": {"$first": "$user.email"}},
                    "count": {"$sum": "$prayer_count"}
                }
            },
            { "$sort" : { "count" : -1 } },
            {
                "$project": {
                    "_id": 0,
                    "name": "$_id.name",
                    "email": "$_id.email",
                    "count": 1
                }
            }
        ])