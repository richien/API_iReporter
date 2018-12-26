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
def do_create(incident):
    incidents_data['data'].append(incident)
    return True


def update(red_flag_id, location=None, comment=None):
    
    for index, data in enumerate(incidents_data['data']):
        if incidents_data['data'][index]['id'] == red_flag_id:
            if location and not comment:
                data['location'] = location
                return data
            elif comment and not location:
                data['comment'] = comment
                return data
        else:
            return None

def do_delete(red_flag_id):
    deleted = False
    for index, data in enumerate(incidents_data['data']):
        if incidents_data['data'][index]['id'] == red_flag_id:
            incidents_data['data'].remove(data)
            deleted =  True
    return deleted

