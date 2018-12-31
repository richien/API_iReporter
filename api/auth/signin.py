from flask import jsonify, request
from flask.views import MethodView
from werkzeug.security import check_password_hash

import data
from api.models.user_model import User
from api.auth.authenticate import Authenticate
from api.views.validator import Validate

users = data.incidents_data["users"]

class Signin(MethodView):

    def post(self):

        request_data = request.get_json()

        try:
            is_valid_request = Validate.validate_signin_request(request_data)
            
            if is_valid_request["is_valid"]:
                if "email" in request_data.keys():
                    email = request_data["email"]
                    username = None
                if "username" in request_data.keys():
                    username = request_data["username"]
                    email=None
                password = request_data["password"]
                user_data = None               
            else:
                message = {
                    "status" : 400,
                    "error" : is_valid_request["message"]
                }
                return jsonify(message), 400

            for index, usr in enumerate(users):        
                if email and usr['email'] == email:
                    user_data = usr
                    break
                elif usr['username'] == username:
                    user_data = usr
                    break

            if user_data:
                user = User(
                                user_id = user_data['id'],
                                firstname=user_data['firstname'],
                                lastname=user_data["lastname"],
                                othernames=user_data["othernames"],
                                email=user_data["email"],
                                phonenumber=user_data["phonenumber"],
                                username=user_data["username"],
                                password=user_data["password"],
                                isAdmin=user_data["isAdmin"]
                            )
                if check_password_hash(user.password, password):
                    token = Authenticate.generate_access_token(user.id, user.isAdmin)
                    message = {
                        "status" : 200,
                        "data" : {
                            "id" : user.id,
                            "message" : f'{email or username} was successfully signed in',
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
                    "error" : f'Unauthorized - User with credentials {email or username} not found'
                }
                return jsonify(message), 401
            
            return jsonify(message), 200

        except Exception as error:
            return jsonify({"status" : 400, "error" : str(error)}), 400
