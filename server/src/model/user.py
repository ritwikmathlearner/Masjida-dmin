from src.db import DB

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