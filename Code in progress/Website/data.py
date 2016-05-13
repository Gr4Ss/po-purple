import time, threading
import os,sys,inspect
#first change the cwd to the script path
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
#append the relative location you want to import from
sys.path.append("../RESTServer")
sys.path.append("../Socket")
from sockets_server import *
from restclient import *
SOCKETPORT = 7002

RESTCLIENT = RestClient("http://192.168.2.21:5000")
#RESTCLIENT = RestClient("http://localhost:9000")
DATA = []
UPDATE_TIME = None
OWN_DATA = None
COMPLETED = []
PARCOURS_ID = None
SOCKET = SocketServer(SOCKETPORT)
SOCKET.start()

def own_data_updater():
    global SOCKET, OWN_DATA
    while True:
        conn,data = SOCKET.get_data()
        SOCKET.send(conn,'OK')
        print data
        if data["Type"] == "Status":
            OWN_DATA = data
        elif data["Type"] == "ParcoursID":
            PARCOURS_ID = data['ID']
        else:
            COMPLETED.append(data["data"])
def get_completed(iden):
    if PARCOURS_ID == iden:
        r = COMPLETED
        COMPLETED = []
        return r
    else:
        return []
def get_own_data():
    global OWN_DATA
    return OWN_DATA
t = threading.Thread(target=own_data_updater)
t.setDaemon(True)
t.start()
def get_index_team(team):
    count = 0
    for d in DATA:
        if d['name'] == team:
            return count
        count += 1
    return -1

def get_data_team(team):
    for d in DATA:
        if d['name'] == team:
            return d
    else:
        return {}
def get_data():
    global DATA,RESTCLIENT,UPDATE_TIME
    if (UPDATE_TIME == None or time.time() - UPDATE_TIME>1.):
        DATA =[]
        parcels = RESTCLIENT.get_parcels()
        on_road_parcels = parcels["on-the-road-parcels"]
        delivered_parcels = parcels["delivered-parcels"]
        positions = RESTCLIENT.get_positions()["positions"]
        for i in range(0,len(positions)):
            update_position(positions[i][0],(positions[i][1],positions[i][2]))
        for j in range(0,len(on_road_parcels)):
            update_on_road_parcel(on_road_parcels[j][3],on_road_parcels[j][:3])
        for k in range(0,len(delivered_parcels)):
            update_delivered_parcels(delivered_parcels[k][3])
        UPDATE_TIME = time.time()
        return DATA
    else:
        return DATA
def update_position(team,position):
    ind = get_index_team(team)
    if ind == -1:
        DATA.append({"name":team,"current_position":position,"current_parcel":None,"deliveries":0})
    else:
        DATA[ind]["current_position"] = position
def update_on_road_parcel(team,parcel_info):
    ind = get_index_team(team)
    if ind == -1:
        DATA.append({"name":team,"current_position":None,"current_parcel":parcel_info,"deliveries":0})
    else:
        DATA[ind]["current_parcel"] = parcel_info
def update_delivered_parcels(team):
    ind = get_index_team(team)
    if ind == -1:
        DATA.append({"name":teamname,"current_position":None,"current_parcel":None,"deliveries":1})
    else:
        DATA[ind]["deliveries"] += 1
