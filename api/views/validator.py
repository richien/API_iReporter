class Validate:

    @staticmethod
    def validate_post_request(request):
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

                 
                