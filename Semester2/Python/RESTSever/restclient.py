import requests
import json
import random
def generate_secret_key(length):
    result = ""
    for i in range(length):
        rand = random.randint(97,122)
        charac = chr(rand)
        result.append(charac)
    return result

class RestClient(object):
    def __init__(self,root,teamname):
        self.__root = root
        self.__secret_key = generate_secret_key(16)
        self.__registed = False
        self.__name = teamname

    def add_team(self):
        resp = requests.post(self.__root + "/robots/"+self.__name,data={"key":self.__secret_key})
        if resp.text == 'OK':
            self.__registed = True
            return True
        else:
            return False
    def get_map(self):
        resp = requests.get(self.__root + "/map")
        return json.loads(resp)
    def get_parcels(self):
        resp = requests.get(self.__root + "/parcels")
        return json.loads(resp)
    def claim_parcel(self, parcel_nb):
        if self.__registed:
            resp = requests.put(self.__root + "/robots/"+self.__name+"/claim/" + str(parcel_nb),data={"key":self.__key})
            return resp.text == 'OK'
        else:
            raise Error('Please add your team first.')
    def deliver_parcel(self, parcel_nb):
        if self.__registed:
            resp = requests.put(self.__root + "/robots/"+self.__name+"/delivered/" + str(parcel_nb),data={"key":self.__key})
            return resp.text == 'OK'
        else:
            raise Error('Please add your team first.')
    def update_position(self, from_node,to_node):
        if self.__registed:
            resp = requests.put(self.__root + "/positions/"+self.__name+"/"+ str(from_node)"/"+str(to_node),data={"key":self.__key})
            return resp.text == 'OK'
        else:
            raise Error('Please add your team first.')
    def get_postions(self):
	    resp = requests.get(self.__root + "/positions")
        return json.loads(resp)
    def get_teamname(self):
	    return self.__name
