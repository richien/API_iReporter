from api.models import incident_model 
from api.models import user_model 

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
                    ],

                        "users" : [

                        ]
    }
def do_create(object, object_dict):

    if type(object) is incident_model.Incident:
        incidents_data['data'].append(object_dict)
        return True
    elif type(object) is user_model.User:
        incidents_data['users'].append(object_dict)
        return True


def update(red_flag_id, location=None, comment=None):

    result = {}
    for index, data in enumerate(incidents_data['data']):
        if incidents_data['data'][index]['id'] == red_flag_id:            
            if location and not comment:
                data['location'] = location
                result = {'data' : data, 'updated' : True}
            elif comment and not location:
                data['comment'] = comment
                result = {'data' : data, 'updated' : True}
    
    return result

def do_delete(red_flag_id):
    
    deleted = False
    for index, data in enumerate(incidents_data['data']):
        if incidents_data['data'][index]['id'] == red_flag_id:
            incidents_data['data'].remove(data)
            deleted =  True
    return deleted

def check_username(username):
    
    exists = False
    for index, user in enumerate(incidents_data['users']):
        if user['username'] == username:
            exists = True 
            break
    return exists

def check_email(email):
    
    exists = False
    for index, user in enumerate(incidents_data['users']):
        if  user['email'] == email:
            exists = True 
            break
    return exists

def do_signin(email):
    
    user = None
    for index, usr in enumerate(incidents_data['users']):
        if check_email(email):
            user = usr
            print(f'USER : {user}')
            break
    return user