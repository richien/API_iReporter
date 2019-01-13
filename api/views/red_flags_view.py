from flask import request, jsonify
from flask.views import MethodView
from api.models.incident_model import Incident
import data
from api.views.validator import Validate

incidents_data = data.incidents_data

class RedFlagsView(MethodView):
    
    
    def get(self, red_flag_id):

        if not red_flag_id:
            red_flags = []
            for data in incidents_data['data']:
                if data['type'].lower() == 'red-flag':
                    red_flag = Incident(**data)
                    red_flags.append(red_flag.to_dict())
            if not red_flags:
                message = {'status': 200, 'data': "No records found" }
            else:
                message = {'status': 200, 'data': red_flags }
        else:
            request_data = request.get_json()
            try:
                if not "red_flag_id" in request_data.keys() or request_data['red_flag_id'] != red_flag_id:
                    error_message = {
                        'status': 400, 
                        'error': "Invalid request - invalid red_flag_id supplied or key error in request body" 
                    }
                    raise KeyError("Invalid request")
                red_flag = None
                for index, data in enumerate(incidents_data['data']):
                    if incidents_data['data'][index]['id'] == red_flag_id:
                        red_flag = Incident(**data)                       
                if red_flag:
                    message = {
                                "status" : 200,
                                "data" : red_flag.to_dict()
                                }
                else:
                    message = {
                                'status': 200, 
                                'data': [ {
                                    "id" : red_flag_id,
                                    "message" : f"No record  with red_flag_id: {red_flag_id} was found" 
                                }]
                    }
            except KeyError as error:
                error_message.update({"error-type":str(error)})  
                return jsonify(error_message), 400
        return jsonify(message), 200

    def post(self):
       
        request_data = request.get_json()
        try:
            validation_result = Validate.validate_incident_post_request(request_data)
            if validation_result["is_valid"]:
                if request_data['type'].lower() == 'red-flag':
                    red_flag = Incident(**request_data)
                    incidents_data['data'].append(red_flag.to_dict())
                    red_flag_id = red_flag.id
                    message = {"status" : 201, 
                                "data" : {
                                        "id" : red_flag_id, 
                                        "message" : "Created red-flag record"
                                        }
                                }
                    return jsonify(message), 201
                else:
                    error_message = {'status' : 400, 'error' : 'Type field should be red-flag'}
                    raise Exception('Invalid request field')
            else:
                error_message = validation_result['message']
                raise Exception("Validation Error")
        except Exception as error:
            error_message.update({"error-type":str(error)})  
            return jsonify(error_message), error_message['status']

    def put(self, red_flag_id):

        request_data = request.get_json()
        try:
            if not "red_flag_id" in request_data.keys() or request_data['red_flag_id'] != red_flag_id:
                error_message = {
                        'status': 400, 
                        'error': "Invalid request - invalid red_flag_id supplied or key error in request body" 
                    }
                raise KeyError("Invalid request")
            red_flag = None
            for index, data in enumerate(incidents_data['data']):
                if incidents_data['data'][index]['id'] == red_flag_id:
                    red_flag = Incident(**data)        
            if not red_flag:
                error_message = {
                            "status" : 404,
                            "error" :  "No record  with ID:{0} was found".format(red_flag_id)
                                }
                raise Exception("Resource Not Found")                
            if 'location' in request_data.keys():    
                if Validate.is_valid_location(request_data['location']):
                    updated_data = red_flag.update_fields(location=request_data['location'])
                    if updated_data:
                        message = {
                                    "status" : 200, 
                                    "data" : {
                                            "id" : red_flag_id,
                                            "message" : "Updated red-flag record's location",
                                            "content" : updated_data
                                            }
                                        }
                else:
                    message = {
                                "status" : 400,
                                "error" : "Failed to update red-flag record's location"
                                    }
            elif 'comment' in request_data.keys():
                if not Validate.is_empty_string(request_data['comment']):
                    updated_data = red_flag.update_fields(comment=request_data['comment'])
                    if updated_data:
                        message = {
                                    "status" : 200, 
                                    "data" : {
                                            "id" : red_flag_id,
                                            "message" : "Updated red-flag record's comment",
                                            "content" : updated_data
                                            }
                                        }
                else:
                    message = {
                                "status" : 400,
                                "error" :  "Failed to update red-flag record's comment"
                                    }
            else:
                message = {
                            "status" : 404,
                            "error" :  "Resource not found -  Invalid field in request body"
                                }
            return jsonify(message), message['status'] 
        except KeyError as error:
            error_message.update({"error-type":str(error)})  
            return jsonify(error_message), 400 
        except Exception as error:
            error_message.update({"error-type":str(error)})  
            return jsonify(error_message), 404    

    def delete(self, red_flag_id):

        request_data = request.get_json()
        try:
            if not "red_flag_id" in request_data.keys() or request_data['red_flag_id'] != red_flag_id:
                error_message = {
                        'status': 400, 
                        'error': "Invalid request - invalid red_flag_id supplied or key error in request body" 
                    }
                raise KeyError("Invalid request body")
            is_deleted = False 
            found = False
            for index, data in enumerate(incidents_data['data']):
                if incidents_data['data'][index]['id'] == red_flag_id:            
                    red_flag = Incident(**data)
                    is_deleted = red_flag.delete_incident()
                    found = True
            if not found:
                error_message = {
                            "status" : 404,
                            "error" : "No record  with ID:{0} was found".format(red_flag_id)
                            }
                raise Exception("Record not found") 
            if is_deleted:
                message = {
                            "status" : 200,
                            "data" : {
                                        "id" : red_flag_id,
                                        "message" : "Red-flag record deleted",                                            
                                        }
                            }
            return jsonify(message), 200           
        except KeyError as error:
            error_message.update({"error-type":str(error)})  
            return jsonify(error_message), 400 
        except Exception as error:
            error_message.update({"error-type":str(error)})  
            return jsonify(error_message), 404 

   