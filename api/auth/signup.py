from flask import jsonify, request
from flask.views import MethodView
from flask_jwt import JWT, current_identity, jwt_required
from werkzeug.security import generate_password_hash

from api.auth.authenticate import Authenticate
from api.models.user_model import User
from api.validator import Validate



class Signup(MethodView):

    def post(self):

        try:
            if request.json:
                request_data = request.get_json()
                validation_result = Validate.validate_signup_details(
                    request_data)
            else:
                error_message = {
                    'status': 400,
                    'error': "Invalid request - request body cannot be empty"
                }
                raise ValueError("Empty request body")
            if validation_result["is_valid"]:
                valid_request = validation_result["request"]
                user = User(**valid_request)
                exists = user.check_user_exists()
                if not exists['exists']:
                    password_hash = generate_password_hash(
                        user.password, method='sha256')
                    user.password = password_hash
                    user_id = user.create_user()
                    user.id = user_id['user_id']
                    token = Authenticate.generate_access_token(
                        user.id, user.isAdmin)
                    
                    message = {
                        "status": 201,
                        "data": [{
                            "id": user.id,
                            "message": "{0} registered successfully".format(user.username),
                            "access_token": token
                        }]
                    }
                else:
                    error_message = {
                        "status": 400,
                        "error": exists["error"]
                    }
                    raise ValueError("Validation error")
            else:
                error_message = {"status": 400}
                error_message.update(validation_result['message'])
                raise Exception("Invalid request")
            return jsonify(message), 201
        except ValueError as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']
        except Exception as error:
            #error_message = {"status": 400}
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']
