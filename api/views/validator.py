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
                     'error': {
                         "message" : "Invalid request body - error in request body, missing required field '{0}'".format(field) 
                         }
                }
                is_valid = False
                break
        return {"is_valid" : is_valid, "message" : message} 

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
                     'error': {
                         "message" : "Invalid request body - error in request body, missing required field '{0}'".format(field) 
                         }
                }
                is_valid = False
                break
            elif Validate.is_empty_string(request['{0}'.format(field)]):
                message = {
                     'status': 400, 
                     'error': {
                         "message" : "Invalid request body -field '{0}' cannot be empty".format(field) 
                         }
                }
                is_valid = False
                break
            elif field == "password" and not User.is_valid_password(request['password']):
                message = {
                     'status': 400, 
                     'error': {
                         "message" : "Password cannot be less than 8 characters" 
                         }
                }
                is_valid = False
                break

        if "othernames" not in request.keys():
            request.update({"othernames" : ""})
        elif "phonenumber" not in request.keys():
            request.update({"phonenumber" : ""})
        elif "isAdmin" not in request.keys():
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
                        'error': {
                            "message" : "Invalid request body - error in request body, missing required field 'username' or 'email" 
                            }
                    }
                is_valid = False
        elif "password" not in request.keys():
            message = {
                     'status': 400, 
                     'error': {
                         "message" : "Invalid request body - error in request body, missing required field 'password'" 
                         }
                }
            is_valid = False
        return {"is_valid" : is_valid, "message" : message} 


                 
                