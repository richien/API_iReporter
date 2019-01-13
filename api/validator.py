from api.models.user_model import User


class Validate:

    @staticmethod
    def validate_incident_post_request(request):
        
        required_fields = [
            "createdBy",
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
                return {"is_valid" : is_valid, "message" : message} 
        if not Validate.is_valid_incident_type(request):
                message = {
                     'status': 400, 
                     'error':  "Invalid request body - invalid Incident type supplied" 
                }
                is_valid = False
        return {"is_valid" : is_valid, "message" : message} 
    
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
                     'error': "Invalid request body -field '{0}' cannot be empty".format(field) 
                }
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
            request.update({"othernames" : ""})
        if "phonenumber" not in request.keys():
            request.update({"phonenumber" : ""})
        if "isAdmin" not in request.keys():
            request.update({"isAdmin" : False}) 
        return {"is_valid" : is_valid, "message" : message, "request" : request}

    @staticmethod
    def is_empty_string(string):

        if string.replace(" ", "") ==  "":
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
                     'error':  "Invalid request body - error in request body, missing required field 'password'"         
                }
            is_valid = False
        return {"is_valid" : is_valid, "message" : message}

    @staticmethod
    def is_valid_location(location):
        latlong = location.split(',')
        if len(latlong) == 2:
            #if float(latlong[0]) in range(-90, 90) and float(latlong[1]) in range(-180, 180):
            is_valid = True
        else:
            is_valid = False
        return is_valid 


                 
                