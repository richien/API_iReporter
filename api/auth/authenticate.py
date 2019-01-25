import datetime
from os import environ

from flask import jsonify, request
from flask_jwt import JWT, current_identity, jwt, jwt_required

from api import app

secret_key = app.config["SECRET_KEY"]


class Authenticate:

    @staticmethod
    def generate_access_token(user_id, isAdmin=False):
        payload = {
            "user_id": user_id,
            "isAdmin": isAdmin,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        }
        token = jwt.encode(payload, secret_key,
                           algorithm="HS256").decode("utf-8")
        return token

    @staticmethod
    def decode_token(token):
        payload = jwt.decode(str(token), secret_key, algorithm="HS256")
        return payload

    @staticmethod
    def retrieve_token_from_request(request):
        auth_header = request.headers.get("Authorization")
        try:
            if not auth_header or "Bearer" not in auth_header:
                error_message = {
                    "status": 400,
                    "error": "Invalid request header - No Authorization header or Bearer token found in request header"
                }
                raise Exception("Invalid request")
            token = str(auth_header).split(" ")[1]
            return token
        except Exception as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']

    @staticmethod
    def get_identity(request):
        return Authenticate.decode_token(
            Authenticate.retrieve_token_from_request(request))["user_id"]

    @staticmethod
    def get_role(request):
        return Authenticate.decode_token(
            Authenticate.retrieve_token_from_request(request))["isAdmin"]
