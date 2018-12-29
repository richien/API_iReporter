from flask import jsonify, request
from flask.views import MethodView
from flask_jwt import JWT, current_identity, jwt_required
from werkzeug.security import generate_password_hash

import data
from api.auth.authenticate import Authenticate
from api.models.user_model import User
from api.views.validator import Validate

users_data = data.incidents_data["users"]

class Signup(MethodView):

    def post(self):

        request_data = request.get_json()
        try:
            validation_result = Validate.validate_signup_details(request_data)
            if validation_result["is_valid"]:
                valid_request = validation_result["request"]
                user = User(
                        firstname=valid_request["firstname"],
                        lastname=valid_request["lastname"],
                        othernames=valid_request["othernames"],
                        email=valid_request["email"],
                        phonenumber=valid_request["phonenumber"],
                        username=valid_request["username"],
                        password=valid_request["password"],
                        isAdmin=valid_request["isAdmin"]
                    )
                if not type(user) is User:
                    message = {
                        "status" : 400,
                        "error" : "User - not created"}
                    return jsonify(message), 400 
                exists = user.check_user_exists()
                if not exists['exists']:
                    password_hash = generate_password_hash(user.password, method='sha256')
                    user.password = password_hash
                    users_data.append(user.to_dict())
                    token = Authenticate.generate_access_token(user.id, user.isAdmin)
                    message = {
                        "status" : 201,
                        "data" : {
                            "id" : user.id,
                            "message" : "{0} registered successfully".format(user.username),
                            "access_token" : token
                            }
                        }
                    return jsonify(message), 201
                else:
                    message = {
                        "status" : 400,
                        "error" : exists["error"]
                    }
                    return jsonify(message), 400
            else:
                return jsonify(validation_result['message']), 400
        except Exception as error:
            return jsonify({"status" : 400, "error": str(error)}), 400
