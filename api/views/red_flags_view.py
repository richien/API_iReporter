from flask import request, jsonify
from flask.views import MethodView
from api.models.incident_model import Incident

incidents_data = { 
                        "data" : [
                            {  
                                "id" : 2,
                                "createdOn" : "12-12-2018",
                                "createdBy" : 5000,
                                "type" : "red-flag",
                                "location" : "33.92300, 44.9084551",
                                "status" : "draft",
                                "images" : ["image_1.png", "image_2.jpg" ],
                                "videos" : ["vid_1.mp4"],
                                "comment" : "Accidental post!",
                                "title": "Roads in poor condition"
                        }
                    ]
    }

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
            if request_data['red_flag_id'] != red_flag_id:
                message = {'status': 400, 'data': "Invalid request body" }
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
            message = {"status" : 201, "data" : red_flag.to_dict()}
            return jsonify(message), 201
        except Exception as error:
            return jsonify(error), 400