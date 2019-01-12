from api.models import incident_model 
from api.models import user_model 

incidents_data = { "data" : [], "users" : [] }

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
    for user in enumerate(incidents_data['users']):
        if user[1]['username'] == username:
            exists = True 
            break
    return exists

def check_email(email):
    
    exists = False
    for user in enumerate(incidents_data['users']):
        if  user[1]['email'] == email:
            exists = True 
            break
    return exists

# def do_signin(email):
    
#     for usr in enumerate(incidents_data['users']):
#         if check_email(email):
#             user = usr[1]
#             break
#     return user