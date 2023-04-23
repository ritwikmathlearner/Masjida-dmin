import json
from bson import json_util
from flask import request, render_template
from src.model.user import UserModel
from src.model.activity import ActivityModel
from datetime import datetime, timedelta

class ViewController:
    __model = None
    __body = None

    def __init__(self) -> None:
        self.__model = UserModel()
    
    def dashboard(self):
        try:
            activities = ActivityModel().index(filter={ 'logout_time': { '$exists': False } })

            for activity in activities:
                last_active_time = activity["login_time"]
                if (last_active := activity.get("last_active", None)):
                    last_active_time = last_active

                if (datetime.utcnow() - last_active_time) > timedelta(minutes=5):
                    new_logout_time = last_active_time + timedelta(minutes=5)
                    ActivityModel().update(
                        { '_id': activity['_id'] },
                        {
                            '$set': { 
                                'logout_time': new_logout_time
                            }
                        }
                    )
            
            if request.args.get('start_date', None) is None and request.args.get('end_date', None) is None:
                loggedinUsers = list(self.__model.loggedinUsers())
                totalPrayer = list(ActivityModel().totalPrayer())
                return render_template('index.html', users=loggedinUsers, prayers=totalPrayer)
            else:
                data = list(self.__model.loggedinUsersFilter(request.args.get('start_date', None), request.args.get('end_date', None)))
                request.args.get('start_date', None)
                return render_template('index.html', users=data, start_date=request.args.get('start_date', None), end_date=request.args.get('end_date', None))
        except Exception as ex:
            print(ex)
            return render_template('error.html')
