from flask.views import MethodView
from flask import jsonify, request
from api.models.user_model import User
import data

users = data.incidents_data["users"]


class UsersView(MethodView):

    def get(self, user_id=None):

        if user_id is None:
            users_list = []
            for usr in enumerate(users):
                user = User(
                    user_id=usr[1]['id'],
                    firstname=usr[1]['firstname'],
                    lastname=usr[1]['lastname'],
                    othernames=usr[1]['othernames'],
                    email=usr[1]['email'],
                    phonenumber=usr[1]['phonenumber'],
                    username=usr[1]['username'],
                    password=usr[1]["password"],
                    registered=usr[1]['registered'],
                    isAdmin=usr[1]['isAdmin']
                )
                users_list.append(user)
            if users_list:
                message = {
                    "status": 200,
                    "data": [{
                        "message": [u.to_dict_minimal() for u in users_list]
                    }]
                }
            else:
                message = {
                    "status": 200,
                    "data": ["There are no users registered"]
                }
        else:
            try:
                user = None
                for usr in enumerate(users):
                    if usr[1]['id'] == user_id:
                        user = User(
                            user_id=usr[1]['id'],
                            firstname=usr[1]['firstname'],
                            lastname=usr[1]['lastname'],
                            othernames=usr[1]['othernames'],
                            email=usr[1]['email'],
                            phonenumber=usr[1]['phonenumber'],
                            username=usr[1]['username'],
                            password=usr[1]["password"],
                            registered=usr[1]['registered'],
                            isAdmin=usr[1]['isAdmin']
                        )
                if user:
                    message = {
                        "status": 200,
                        "data": [{
                            "id": user_id,
                            "message": user.to_dict_minimal()
                        }]
                    }
                else:
                    message = {'status': 200, 'data': [
                        f'No user with ID: {user_id} was found']}
            except Exception as error:
                error_message = {
                        'status': 400,
                        'error': error
                    }
                return jsonify(error_message), error_message['status']
        return jsonify(message), message['status']
