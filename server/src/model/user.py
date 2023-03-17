from src.db import DB
from datetime import datetime, timedelta

class UserModel:
    collection_name = 'users'
    __collection = None
    __db = None

    def __init__(self) -> None:
        self.__db = DB().db()
        self.__collection = self.__db[self.collection_name]

    def index(self):
        users = list(self.__collection.find({
            "verification_otp": {
                "$exists": False
            }
        }))
        return users
    
    def create(self, data):
        new_user_id = self.__collection.insert_one(data).inserted_id
        return new_user_id
    
    def get_single(self, email):
        user = self.__collection.find_one({
            "email": email
        })
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
        self.__collection.update_one(query, data)

    def loggedinUsers(self):
        return self.__collection.aggregate(
            [
                {
                    "$match": {
                        "verification_otp": { "$exists": False }
                    }
                },
                {
                    "$lookup": {
                        "from": "activities",
                        "localField": "_id",
                        "foreignField": "ref_id",
                        "pipeline": [
                            {
                                "$match": {
                                    "logout_time": { "$exists": False }
                                }
                            }
                        ],
                        "as": "active",
                    },
                },
                {
                    "$unwind": {
                        "path": "$active",
                        "preserveNullAndEmptyArrays": False
                    }
                },
                {
                    "$project": {
                        "name": 1,
                        "email": 1,
                        "active.login_time": 1
                    }
                }
            ]
        )

    def loggedinUsersFilter(self, start_date, end_date):
        format = f'%Y-%m-%d'
        start_date = datetime.strptime(start_date, format) + timedelta()
        end_date = datetime.strptime(end_date, format) + timedelta(hours=23, minutes=59, seconds=59)
        print(type(start_date), end_date)
        return self.__collection.aggregate(
            [
                {
                    "$match": {
                        "verification_otp": { "$exists": False }
                    }
                },
                {
                    "$lookup": {
                        "from": "activities",
                        "localField": "_id",
                        "foreignField": "ref_id",
                        "pipeline": [
                            {
                                "$match": {
                                    "login_time": { "$gte": start_date, "$lte": end_date }
                                }
                            }
                        ],
                        "as": "active",
                    },
                },
                {
                    "$unwind": {
                        "path": "$active",
                        "preserveNullAndEmptyArrays": False
                    }
                },
                {
                    "$project": {
                        "name": 1,
                        "email": 1,
                        "active.login_time": 1,
                        "active.logout_time": 1
                    }
                }
            ]
        )