import datetime
from os import environ

from flask import jsonify, request
from flask_jwt import JWT, current_identity, jwt, jwt_required


from api import app

secret_key = app.config["SECRET_KEY"]


class Authenticate:

    @staticmethod
    def generate_access_token(user_id, isAdmin=False):
        try:
            payload = {
                "user_id": user_id,
                "isAdmin": isAdmin,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
            }
            token = jwt.encode(payload, secret_key,
                            algorithm="HS256").decode("utf-8")
            return token
        except Exception as error:
            return error

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(str(token), secret_key, algorithm="HS256")
            return payload
        except jwt.ExpiredSignatureError:
            return {'error': 'Signature expired. Please login again.', 'user_id': None, 'isAdmin': None}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token. Please login again.', 'user_id': None, 'isAdmin': None}

    @staticmethod
    def retrieve_token_from_request(request):
        response = {"error": None}
        auth_header = request.headers.get("Authorization")
        try:
            if not auth_header or "Bearer" not in auth_header:
                error = {
                    "status": 401,
                    "error-type": "Unauthorized - No Authorization header or Bearer token found in request header"
                }
                response.update(error)
                raise Exception("Unauthorized")
            token = str(auth_header).split(" ")[1]
            response.update({"token": token})
        except Exception as error:
            response.update({"error": str(error)})
        return response

    @staticmethod
    def get_identity(token):
        try:
            decoded_token =  Authenticate.decode_token(token)
            if decoded_token['user_id']:
                return {'user_id': decoded_token["user_id"], 'error': None}
            else:
                raise Exception(decoded_token['error'])
        except Exception as error:
            return {'error': str(error)}

    @staticmethod
    def get_role(token):
        try:
            decoded_token =  Authenticate.decode_token(token)
            if decoded_token['user_id']:
                return {'isAdmin': decoded_token["isAdmin"], 'error': None}
            else:
                raise Exception(decoded_token['error'])
        except Exception as error:
            return {'error': str(error)}
