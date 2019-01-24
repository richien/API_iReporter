from flask import jsonify, request
from flask.views import MethodView
from werkzeug.security import check_password_hash

import data
from api.models.user_model import User
from api.auth.authenticate import Authenticate
from api.validator import Validate
from api.models.database import userdb_api



class Signin(MethodView):

    def post(self):

        try:
            error_message = {"status": 400}
            if request.json:
                request_data = request.get_json()
                is_valid_request = Validate.validate_signin_request(
                    request_data)
            else:
                error_message = {
                    'status': 400,
                    'error': "Invalid request - request body cannot be empty"
                }
                raise ValueError("Empty request body")
            email = None
            username = None
            if is_valid_request["is_valid"]:             
                if "email" in request_data.keys():
                    email = request_data["email"]
                    email_exists = userdb_api.check_email_exists(email)
                    username_exists = None
                if "username" in request_data.keys():
                    username = request_data["username"]
                    username_exists = userdb_api.check_username_exists(username)
                    email_exists = None
                password = request_data["password"]
                user_data = None
            else:
                error_message = {"status": 400}
                error_message.update(is_valid_request["message"])
                raise ValueError("Invalid request")

            if email and email_exists:
                user_data = email_exists 
            elif username_exists:
                user_data = username_exists

            if user_data:
                user = User(
                    user_id=user_data['user_id'],
                    firstname=user_data['firstname'],
                    lastname=user_data["lastname"],
                    othernames=user_data["othernames"],
                    email=user_data["email"],
                    phonenumber=user_data["phonenumber"],
                    username=user_data["username"],
                    registered=user_data["registered"],
                    password=user_data["password"],
                    isAdmin=user_data["isadmin"]
                )
                if check_password_hash(user.password, password):
                    token = Authenticate.generate_access_token(
                        user.id, user.isAdmin)
                    message = {
                        "status": 200,
                        "data": [{
                            "user": user.to_dict_minimal(),
                            "access_token": token
                        }]
                    }
                else:
                    error_message = {
                        "status": 401,
                        "error": "Unauthorized - Wrong login credentials supplied - Try again"}
                    raise Exception("Unauthorized")
            else:
                error_message = {
                    "status": 401,
                    "error": f'Unauthorized - User with credentials {email or username} not found'}
                raise Exception("Unauthorized")
            return jsonify(message), 200
        except ValueError as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']
        except Exception as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']
