import datetime
from os import environ
from flask_jwt import jwt
from flask import request, jsonify

secret_key = "esi5xKgrycPdTE5f9d1"

class Authenticate:

    @staticmethod
    def generate_access_token(user_id, isAdmin=False):
        payload = {
            "user_id" : user_id,
            "isAdmin" : isAdmin,
            "iat" : datetime.datetime.utcnow(),
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256").decode("utf-8")
        return token

    @staticmethod
    def decode_token(token):
        payload = jwt.decode(str(token), secret_key, algorithms="HS256")
        return payload

    @staticmethod
    def retrieve_token_from_request(request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or "Bearer" not in auth_header:
            message = {
                "status" : 400,
                "error" : "Invalid request header - No Authorization header or Bearer token found in request header"
            }
            return jsonify(message), 400
        token = str(auth_header).split(" ")[1]
        return token

    @staticmethod
    def get_identity(request):
        return Authenticate.decode_token(Authenticate.retrieve_token_from_request(request))["user_id"]

    @staticmethod
    def get_role(request):
        return Authenticate.decode_token(Authenticate.retrieve_token_from_request(request))["isAdmin"]