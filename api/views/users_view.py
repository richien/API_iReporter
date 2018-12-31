from flask.views import MethodView
from flask import jsonify, request
from api.models.user_model import User
import data

users_data = data.incidents_data["users"]

class UsersView(MethodView):


    def get(self):

        users = []

        try:
            for index, usr in enumerate(users_data):
                user = User(
                    user_id=usr['id'],
                    firstname=usr['firstname'],
                    lastname=usr['lastname'],
                    othernames=usr['othernames'],
                    email=usr['email'],
                    phonenumber=usr['phonenumber'],
                    username=usr['username'],
                    password=usr["password"],
                    registered=usr['registered'],
                    isAdmin=usr['isAdmin']
                )
                users.append(user)

            print(f'USERS LIST: {users}')
            if users:
                print(f'USERS LIST: {users}')
                message = {
                    "status" : 200,
                    "data" : {
                        "message" : [u.to_dict() for u in users]
                    }
                }
                return jsonify(message), 200
            else:
                message = {
                    "status" : 200,
                    "error" : "There are no users registered"
                }
                return jsonify(message), 200
        
        except Exception as e:
            message = {
                "status" : 400,
                "error" : str(e)
            }
            return jsonify(message), 400