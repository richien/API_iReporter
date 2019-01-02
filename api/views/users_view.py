from flask.views import MethodView
from flask import jsonify, request
from api.models.user_model import User
import data

users = data.incidents_data["users"]

class UsersView(MethodView):


    def get(self, user_id=None):

        if user_id is None:
            users_list = []
            try:
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
                        "status" : 200,
                        "data" : {
                            "message" : [u.to_dict_minimal() for u in users_list]
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

        else:

            request_data = request.get_json()
            if not "user_id" in request_data.keys() or request_data['user_id'] != user_id:
                message = {
                    'status' : 400,
                    'error' : {
                        'id' : user_id,
                        'message' : "Invalid request - invalid user_id supplied or key error in request body"
                    }
                }
                return jsonify(message), 400
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
                        if not type(user) is User:
                            message = {
                                'status' : 400,
                                'error' : {
                                    'id' : user_id,
                                    'message' : 'User not created'
                                }
                            }
                            return jsonify(message)

                if user:
                    message = {
                        "status" : 200,
                        "data" : {
                            "id" : user_id,
                            "message" : user.to_dict_minimal()
                        }
                    }
                    return jsonify(message), 200
                else:
                    message = {'status' : 200, 'error' : f'No user with ID: {user_id} was found'}
                    return jsonify(message), 200
            except Exception as error:
                message = {
                    'status' : 400,
                    'error' : error
                }
                return jsonify(message), 400