import json
from bson import json_util
from flask import request, render_template
from src.model.user import UserModel
from src.model.activity import ActivityModel

class ViewController:
    __model = None
    __body = None

    def __init__(self) -> None:
        self.__model = UserModel()
    
    def dashboard(self):
        try:
            if request.args.get('start_date', None) is None and request.args.get('end_date', None) is None:
                loggedinUsers = list(UserModel().loggedinUsers())
                totalPrayer = list(ActivityModel().totalPrayer())
                return render_template('index.html', users=loggedinUsers, prayers=totalPrayer)
            else:
                data = list(UserModel().loggedinUsersFilter(request.args.get('start_date', None), request.args.get('end_date', None)))
                request.args.get('start_date', None)
                return render_template('index.html', users=data, start_date=request.args.get('start_date', None), end_date=request.args.get('end_date', None))
        except Exception as ex:
            print(ex)
