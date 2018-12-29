from flask import jsonify, request
from flask.views import MethodView
from werkzeug.security import check_password_hash

import data
from api.models.user_model import User
from api.auth.authenticate import Authenticate

users_data = data.incidents_data["users"]

class Signin(MethodView):

    def post(self):

        request_data = request.get_json()

        try:

            email = request_data["email"]
            password = request_data["password"]

            user_data = data.do_signin(email)
            print(f'USER_DATA : {user_data}')
            if user_data:
                user = User(
                                id = user_data['id'],
                                firstname=user_data['firstname'],
                                lastname=user_data["lastname"],
                                othernames=user_data["othernames"],
                                email=user_data["email"],
                                phonenumber=user_data["phonenumber"],
                                username=user_data["username"],
                                password=user_data["password"],
                                isAdmin=user_data["isAdmin"]
                            )
                print(f'USER_OBJ : {user.to_dict()}')
                if check_password_hash(user.password, password):
                    token = Authenticate.generate_access_token(user.id, user.isAdmin)
                    message = {
                        "status" : 200,
                        "data" : {
                            "id" : user.id,
                            "message" : f'{email} was successfully signed in',
                            "access_token" : token
                        }
                    }
                else:
                    message = {
                        "status" : 401,
                        "error" : "Unauthorized - Wrong signin credentials supplied - Try again"
                    }
                    return jsonify(message), 401

            else:
                message = {
                    "status" : 401,
                    "error" : f'Unauthorized - User with email {email} not found'
                }
                return jsonify(message), 401
            
            return jsonify(message), 200

        except Exception as error:
            return jsonify({"status" : 400, "error" : str(error)}), 400
