from datetime import datetime
import time,threading
import os,sys,inspect
#first change the cwd to the script path
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
#append the relative location you want to import from
sys.path.append("../RESTServer")

from restclient import *
class Data:
    def __init__(self):
        self.data = []
        self.restclient = RestClient("http://localhost:9000")
        self.delivered_count = 0
        self.going = False
        self.thread = threading.Thread(target=self.updater)
    def start(self):
        if not self.going:
            self.going = True
            self.thread.setDaemon(True)
            self.thread.start()
    def stop(self):
        self.going = False
        self.thrad.join()
    def get_teams(self):
        r = []
        for d in self.data:
            r.append(d['name'])
        return r
    def get_index_team(self,team):
        count = 0
        for d in self.data:
            if d['name'] == team:
                return count
            count += 1
        return -1
    def get_data_team(self,team):
        for d in self.data:
            if d['name'] == team:
                return d
    def get_data(self):
        return self.data
    def add_delivery(self,teamname,parcel_nb):
        ind = self.get_index_team(teamname)
        if ind == -1:
            self.data.append({"name":teamname,"positions":[],"deliveries":[[str(datetime.now()),parcel_nb]]})
        else:
            self.data[ind]["deliveries"].append([str(datetime.now()),parcel_nb])

    def add_position(self,teamname,position):
        ind = self.get_index_team(teamname)
        if ind == -1:
            self.data.append({"name":teamname,"positions":[[str(datetime.now()),position]],"deliveries":[]})
        elif self.data[ind]["positions"][-1][1] != position:
            self.data[ind]["positions"].append([str(datetime.now()),position])
    def updater(self):
        while self.going:
            delivered_parcels = self.restclient.get_parcels()["delivered-parcels"]
            positions = self.restclient.get_positions()["positions"]
            for i in range(0,len(positions)):
                self.add_position(positions[i][0],(positions[i][1],positions[i][2]))
            for j in range(self.delivered_count,len(delivered_parcels)):
                self.add_delivery(delivered_parcels[j][-1],delivered_parcels[j][0])
            self.delivered_count = len(delivered_parcels)
            time.sleep(1)
