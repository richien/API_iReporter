from api.models.user_model import User
from flask import g, jsonify
from api.auth.authenticate import Authenticate


class Validate:

    @staticmethod
    def validate_incident_post_request(request):

        required_fields = [
            "createdby",
            "type",
            "location",
            "status",
            "title",
            "images",
            "videos",
            "comment"
        ]
        is_valid = True
        message = None
        for field in required_fields:
            if field not in request.keys():
                message = {
                    'status': 400,
                    'error': "Invalid request body - error in request body, missing required field '{0}'".format(field)
                }
                is_valid = False
                return {"is_valid": is_valid, "message": message}
        if not Validate.is_valid_incident_type(request):
            message = {
                'status': 400,
                'error': "Invalid request body - invalid Incident type supplied"}
            is_valid = False
        return {"is_valid": is_valid, "message": message}

    @staticmethod
    def is_valid_incident_type(request):

        is_valid = True
        if request['type'].lower() not in ['red-flag', 'intervention']:
            is_valid = False
        return is_valid

    @staticmethod
    def validate_signup_details(request):

        required_fields = [
            "firstname",
            "lastname",
            "email",
            "username",
            "password"
        ]
        is_valid = True
        message = None
        for field in required_fields:
            if field not in request.keys():
                message = {
                    'status': 400,
                    'error': "Invalid request body - error in request body, missing required field '{0}'".format(field)
                }
                is_valid = False
                break
            elif Validate.is_empty_string(request['{0}'.format(field)]):
                message = {
                    'status': 400,
                    'error': "Invalid request body -field '{0}' cannot be empty".format(field)}
                is_valid = False
                break
            elif field == "password" and not User.is_valid_password(request['password']):
                message = {
                    'status': 400,
                    'error': "Password cannot be less than 8 characters"
                }
                is_valid = False
                break
        if "othernames" not in request.keys():
            request.update({"othernames": ""})
        if "phonenumber" not in request.keys():
            request.update({"phonenumber": ""})
        if "isAdmin" not in request.keys():
            request.update({"isAdmin": False})
        return {"is_valid": is_valid, "message": message, "request": request}

    @staticmethod
    def is_empty_string(string):

        if string.replace(" ", "") == "":
            return True
        else:
            return False

    @staticmethod
    def validate_signin_request(request):

        is_valid = True
        message = None
        if "email" not in request.keys():
            if "username" not in request.keys():
                message = {
                    'status': 400,
                    'error': "Invalid request body - error in request body, missing required field 'username' or 'email"
                }
                is_valid = False
        if "password" not in request.keys():
            message = {
                'status': 400,
                'error': "Invalid request body - error in request body, missing required field 'password'"
            }
            is_valid = False
        return {"is_valid": is_valid, "message": message}

    @staticmethod
    def is_valid_location(location):
        latlong = location.split(',')
        if len(latlong) == 2:
            is_valid = True
        else:
            is_valid = False
        return is_valid
    
    @staticmethod
    def is_valid_status(status):
        expected = [
            'under-investigation',
            'resolved',
            'rejected'
        ]
        if status in expected:
            is_valid = True
        else:
            is_valid = False
        return is_valid

    @staticmethod
    def validate_token(token):
        """
        Check whether a token is valid and create a global variable
        with the user's ID and role.
        Return boolean
        """
        valid = {'is_valid': True, 'status': None, 'error': None}
        try:
            g.user_id = None
            g.isAdmin = None
            if  not token['error']: 
                identity = Authenticate.get_identity(token['token'])
                if not identity['error']:
                    g.user_id = identity['user_id']
                    g.isAdmin = Authenticate.get_role(token['token'])['isAdmin']
                else:
                    raise Exception(identity['error'])
            else:
                raise Exception(token['error-type'])
        except Exception as error:
            valid = {'is_valid': False, 'status': 401, 'error': str(error)}
        return valid

    @staticmethod
    def validate_request(request):
        validation_result = {'is_valid': False, 'message': None}
        try:
            if request.json:
                request_data = request.get_json()
                validation_result = Validate.validate_incident_post_request(
                    request_data)
            else:
                error_message = {
                    'status': 400,
                    'error': "Invalid request - request body cannot be empty"}
                raise ValueError("Empty request body")
        except ValueError as error:
            validation_result.update({"message": error_message, "error": str(error)})
        return validation_result

    @staticmethod
    def validate_request_body(request):
        validation_result = {'is_valid': False, 'message': None}
        try:
            if request.json:
                validation_result['is_valid'] = True
            else:
                error_message = {
                    'status': 400,
                    'error': "Invalid request - request body cannot be empty"}
                raise ValueError("Empty request body")
        except ValueError as error:
            validation_result.update({"message": error_message, "error": str(error)})
        return validation_result
