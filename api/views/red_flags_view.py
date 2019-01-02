from flask import request, jsonify
from flask.views import MethodView
from api.models.incident_model import Incident
import data
from api.views.validator import Validate

incidents_data = data.incidents_data

class RedFlagsView(MethodView):
    
    
    def get(self, red_flag_id):

        if red_flag_id is None:
            red_flags_list = []
            for data in incidents_data['data']:
                if data['type'] == 'red-flag':
                    red_flag = Incident(createdBy=data['createdBy'], type=data['type'],
                    location=data['location'], status=data['status'], images=data['images'],
                    videos=data['videos'], comment=data['comment'], title=data['title'], 
                    id=data['id'], createdOn=data['createdOn'])
                    red_flags_list.append(red_flag.to_dict())
            if not red_flags_list:
                message = {'status': 200, 'data': "No records found" }
                return jsonify(message)
            message = {'status': 200, 'data': red_flags_list }
            return jsonify(message)
        else:
            request_data = request.get_json()
            if not "red_flag_id" in request_data.keys() or request_data['red_flag_id'] != red_flag_id:
                message = {
                    'status': 400, 
                    'error': {
                        "id" : red_flag_id,
                        "message" : "Invalid request - invalid red_flag_id supplied or key error in request body" 
                        }
                }
                return jsonify(message), 400
            try:
                red_flag = None
                for index, data in enumerate(incidents_data['data']):
                    if incidents_data['data'][index]['id'] == red_flag_id:
                            red_flag = Incident(id = red_flag_id, createdBy=data['createdBy'], type=data['type'],
                                    location=data['location'], status=data['status'], images=data['images'],
                                    videos=data['videos'], comment=data['comment'], title=data['title'])
                            if not type(red_flag) is Incident:
                                message = {
                                    "status" : 400, 
                                    "error" : {
                                        "id" : red_flag_id, 
                                        "message" : "Incident not created!"
                                    }
                                }
                                return jsonify(message)
                if red_flag:
                    message = {
                                "status" : 200,
                                "data" : red_flag.to_dict()
                                }
                    return jsonify(message), 200
                else:
                        message = {'status': 200, "error": "No record  with red_flag_id: {0} was found".format(red_flag_id) }
                        return jsonify(message), 200                  
            except Exception as error:
                return jsonify(error), 400

    def post(self):
       
        request_data = request.get_json()
        try:
            validation_result = Validate.validate_incident_post_request(request_data)
            if validation_result["is_valid"]:
                red_flag = Incident(createdBy=request_data['createdBy'], type=request_data['type'],
                location=request_data['location'], status=request_data['status'], images=request_data['images'],
                videos=request_data['videos'], comment=request_data['comment'], title=request_data['title'])
                if not type(red_flag) is Incident:
                    message = {"status" : 400, "data" : "Incident[Red-flag] - not created"}
                    return jsonify(message), 400
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
                return jsonify(validation_result['message']), 400
        except Exception as error:
            return jsonify(error), 400

    def put(self, red_flag_id):

        request_data = request.get_json()
        if not "red_flag_id" in request_data.keys() or request_data['red_flag_id'] != red_flag_id:
                message = {
                    'status': 400, 
                    'error': {
                        "id" : red_flag_id,
                        "message" : "Invalid request - invalid red_flag_id supplied or key error in request body" 
                        }
                }
                return jsonify(message), 400
        try:
            red_flag = None
            for index, data in enumerate(incidents_data['data']):
                if incidents_data['data'][index]['id'] == red_flag_id:
                    red_flag = Incident(id = red_flag_id, createdBy=data['createdBy'], type=data['type'],
                                location=data['location'], status=data['status'], images=data['images'],
                                videos=data['videos'], comment=data['comment'], title=data['title'])
                    if not type(red_flag) is Incident:
                        message = {"status" : 400, "error" : {"id" : red_flag_id, "message" : "Incident not created!"}}
                        return jsonify(message)
            
            if not red_flag:
                message = {
                            "status" : 404,
                            "error" : {
                                    "id" : red_flag_id, 
                                    "message" : "No record  with ID: {0} was found".format(red_flag_id)
                                    }
                                }
                return jsonify(message), 404
                
            if 'location' in request_data.keys():    
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
                    return jsonify(message), 200
                else:
                    message = {
                                "status" : 400,
                                "error" : {
                                        "id" : red_flag_id,
                                        "message" : "Failed to update red-flag record's location"
                                                }
                                    }
                    return jsonify(message), 400
            elif 'comment' in request_data.keys():
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
                    return jsonify(message), 200
                else:
                    message = {
                                "status" : 400,
                                "error" : {
                                        "id" : red_flag_id,
                                        "message" : "Failed to update red-flag record's comment"
                                            }
                                    }
                    return jsonify(message), 400
            else:
                message = {
                                "status" : 404,
                                "error" : {
                                        "id" : red_flag_id,
                                        "message" : "Resource not found -  Invalid resource in request body"
                                            }
                                    }
                return jsonify(message), 404   
        except Exception as error:
            return jsonify(error), 400    

    def delete(self, red_flag_id):

        request_data = request.get_json()
        if not "red_flag_id" in request_data.keys() or request_data['red_flag_id'] != red_flag_id:
                message = {
                    'status': 400, 
                    'error': {
                        "id" : red_flag_id,
                        "message" : "Invalid request - invalid red_flag_id supplied or key error in request body" 
                        }
                }
                return jsonify(message), 400
        try:
            is_deleted = False 
            found = False
            for index, data in enumerate(incidents_data['data']):
                if incidents_data['data'][index]['id'] == red_flag_id:            
                    red_flag = Incident(id = red_flag_id, createdBy=data['createdBy'], type=data['type'],
                                        location=data['location'], status=data['status'], images=data['images'],
                                        videos=data['videos'], comment=data['comment'], title=data['title'])
                    is_deleted = red_flag.delete_incident()
                    found = True
            if not found:
                message = {
                            "status" : 404,
                            "error" : {
                                "id" : red_flag_id,
                                "message" : "No record  with ID: {0} was found".format(red_flag_id)
                                }
                            }
                return jsonify(message), 404 
            if is_deleted:
                message = {
                            "status" : 200,
                            "data" : {
                                        "id" : red_flag_id,
                                        "message" : "Red-flag record deleted",                                            
                                        }
                            }
                return jsonify(message), 200
            else:
                message = {
                            "status" : 200,
                            "data" : {
                                    "id" : red_flag_id,
                                    "message" : "Delete error: Record found but not deleted"
                                        }
                            }
                return jsonify(message), 200           
        except Exception as error:
            message = {
                        "status" : 400,
                        "error" : {
                            "id" : red_flag_id,
                            "message" : str(error)
                            }
                        }
            return jsonify(message), 400

   