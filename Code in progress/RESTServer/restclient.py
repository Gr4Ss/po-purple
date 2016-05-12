import requests
import json
import random
def generate_secret_key(length):
    result = '%030x' % random.randrange(16**100)
    return '0x' + result

class RestClient(object):
    def __init__(self,root,teamname = None):
        self.__root = root
        self.__secret_key = generate_secret_key(16)
        self.__registed = False
        self.__name = teamname

    def add_team(self):
        resp = requests.post(self.__root + "/robots/"+self.__name,data=self.__secret_key)
        print resp.text
        if resp.text == 'OK':
            self.__registed = True
            return True
        else:
            return False
    def get_map(self):
        resp = requests.get(self.__root + "/map")
        return resp.json()

    def get_parcels(self):
        resp = requests.get(self.__root + "/parcels")

        return resp.json()
    def claim_parcel(self, parcel_nb):
        if not isinstance(parcel_nb,int):
            raise Exception('Parcel number must be int')
        if self.__registed:
            resp = requests.put(self.__root + "/robots/"+self.__name+"/claim/" + str(parcel_nb),data=self.__secret_key)
            return resp.text == 'OK'
        else:
            raise Error('Please add your team first.')
    def deliver_parcel(self, parcel_nb):
        if not isinstance(parcel_nb,int):
            raise Exception('Parcel number must be int')
        if self.__registed:
            resp = requests.put(self.__root + "/robots/"+self.__name+"/delivered/" + str(parcel_nb),data=self.__secret_key)
            return resp.text == 'OK'
        else:
            raise Error('Please add your team first.')
    def update_position(self, from_node,to_node):
        if self.__registed:
            resp = requests.put(self.__root + "/positions/"+self.__name+"/"+ str(from_node)+"/"+str(to_node),data=self.__secret_key)
            return resp.text == 'OK'
        else:
            raise Error('Please add your team first.')
    def get_positions(self):
		resp = requests.get(self.__root + "/positions")
		return resp.json()
    def get_teamname(self):
	    return self.__name
