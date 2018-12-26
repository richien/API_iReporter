from flask import request, jsonify
from flask.views import MethodView
from api.models.incident_model import Incident
import data

incidents_data = data.incidents_data

class RedFlagsView(MethodView):
    
    
    def get(self, red_flag_id):

        if red_flag_id is None:
            json_red_flags = []
            for data in incidents_data['data']:
                if data['type'] == 'red-flag':
                    red_flag = Incident(createdBy=data['createdBy'], type=data['type'],
                    location=data['location'], status=data['status'], images=data['images'],
                    videos=data['videos'], comment=data['comment'], title=data['title'], 
                    id=data['id'], createdOn=data['createdOn'])
                    json_red_flags.append(red_flag.to_dict())
            if not json_red_flags:
                message = {'status': 200, 'data': "No records found" }
                return jsonify(message)
            message = {'status': 200, 'data': json_red_flags }
            return jsonify(message)
        else:
            request_data = request.get_json()
            if not "red_flag_id" in request_data.keys() or request_data['red_flag_id'] != red_flag_id:
                message = {'status': 400, 'data': "Invalid request - red_flag_id not supplied or key error in request body" }
                return jsonify(message), 400
            red_flag_data = None
            try:
                index = 0
                while index < len(incidents_data['data']):
                    if incidents_data['data'][index]['id'] == red_flag_id:
                        data = incidents_data['data'][index]
                    index += 1
                if data:
                        red_flag = Incident(createdBy=data['createdBy'], type=data['type'],location=data['location'],
                         status=data['status'], images=data['images'],videos=data['videos'], comment=data['comment'], 
                         title=data['title'], id=data['id'], createdOn=data['createdOn'])
                        message = {'status': 200, 'data': red_flag.to_dict() }
                        return jsonify(message), 200
                else:
                    message = {'status': 404, 'data': "No record  with red_flag_id: {0} was found".format(red_flag_id) }
                    return jsonify(message), 404
            except Exception as error:
                return jsonify(error), 400

    def post(self):
       
        request_data = request.get_json()
        try:
            if 'createdBy' not in request_data.keys() or 'type' not in request_data.keys() or 'location' not in request_data.keys() or 'status' not in request_data.keys() or 'title' not in request_data.keys():         
                message = {"status" : 400, "data" : "Invalid request body - Required fields missing in request body"}
                return jsonify(message), 400
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
        except Exception as error:
            return jsonify(error), 400

    def put(self, red_flag_id):

        request_data = request.get_json()
        if request_data['red_flag_id'] != red_flag_id:
            message = {'status': 400, 'data': "Invalid request body" }
            return jsonify(message), 400
        try:
            for index, data in enumerate(incidents_data['data']):
                if incidents_data['data'][index]['id'] == red_flag_id:
                        red_flag = Incident(id = red_flag_id, createdBy=data['createdBy'], type=data['type'],
                                location=data['location'], status=data['status'], images=data['images'],
                                videos=data['videos'], comment=data['comment'], title=data['title'])
                        if not type(red_flag) is Incident:
                            message = {"status" : 400, "data" : {"id" : red_flag_id, "message" : "Incident not created!"}}
                            return jsonify(message)
                        if request_data['location']:    
                            updated_data = red_flag.update_fields(location=request_data['location'])
                            if updated_data:
                                message = {
                                            "status" : 200, 
                                            "data" : {
                                                    "id" : red_flag_id,
                                                    "message" : "Updated red-flag record's location"
                                                    }
                                                }
                                return jsonify(message), 200
                            else:
                                message = {
                                            "status" : 400,
                                            "data" : {
                                                    "id" : red_flag_id,
                                                    "message" : "Failed to update red-flag record's location"
                                                        }
                                                }
                                return jsonify(message), 400

                else:
                    message = {
                                "status" : 404,
                                "data" : {
                                        "id" : red_flag_id, 
                                        "message" : "No record  with ID: {0} was found".format(red_flag_id)
                                        }
                                    }
                    return jsonify(message), 404
        except Exception as error:
            return jsonify(error), 400    
            