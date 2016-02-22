import requests
import json
import random
root = "http://localhost:8080"
def generate_secret_key(length):
    result = ""
    for i in range(length):
        rand = random.randint(97,122)
        charac = chr(rand)
        result.append(charac)
    return result
SECRETKEY = None
REGISTED = False
NAME = None

def add_team(name):
    key = generate_secret_key(16)
    resp = requests.post(root + "/robots/"+name,data={"key":key})
    if resp.text == 'OK':
        REGISTED = True
        SECRETKEY = key
        NAME = name
        return True
    else:
        return False
def get_map():
    resp = requests.get(root + "/map")
    return json.loads(resp)
def get_parcels():
    resp = requests.get(root + "/parcels")
    return json.loads(resp)
def claim_parcel(parcel_nb):
    if REGISTED:
        resp = requests.put(root + "/robots/"+NAME+"/claim/" + str(parcel_nb),data={"key":SECRETKEY})
        return resp.text == 'OK'
    else:
        raise Error('Please add your team first.')
def deliver_parcel(parcel_nb):
    if REGISTED:
        resp = requests.put(root + "/robots/"+NAME+"/delivered/" + str(parcel_nb),data={"key":SECRETKEY})
        return resp.text == 'OK'
    else:
        raise Error('Please add your team first.')
def update_position(from_node,to_node):
    if REGISTED:
        resp = requests.put(root + "/positions/"+NAME+"/"+ str(from_node)"/"+str(to_node),data={"key":SECRETKEY})
        return resp.text == 'OK'
    else:
        raise Error('Please add your team first.')
