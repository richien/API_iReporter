from flask import jsonify, request
from flask.views import MethodView
from werkzeug.security import check_password_hash

import data
from api.models.user_model import User
from api.auth.authenticate import Authenticate
from api.validator import Validate

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
                error_message = { "status" : 400 }
                error_message.update(is_valid_request["message"])
                raise ValueError("Invalid request")
            for usr in enumerate(users):        
                if email and usr[1]['email'] == email:
                    user_data = usr[1]
                    break
                elif usr[1]['username'] == username:
                    user_data = usr[1]
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
                        "data" : [{
                            "id" : user.id,
                            "message" : f'{email or username} was successfully signed in',
                            "access_token" : token
                        }]
                    }
                else:
                    error_message = {
                        "status" : 401,
                        "error" : "Unauthorized - Wrong signin credentials supplied - Try again"
                    }
                    raise Exception("Unauthorized")
            else:
                error_message = {
                    "status" : 401,
                    "error" : f'Unauthorized - User with credentials {email or username} not found'
                }
                raise Exception("Unauthorized")   
            return jsonify(message), 200
        except ValueError as error:
            error_message.update({"error-type":str(error)})  
            return jsonify(error_message), error_message['status']
        except Exception as error:
            error_message.update({"error-type":str(error)})  
            return jsonify(error_message), error_message['status']
        
