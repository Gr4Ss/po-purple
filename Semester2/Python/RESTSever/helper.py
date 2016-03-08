import json
# |----------------------------------------------------------------------------|
# |TODO:  - Documentatie                                                       |
# |       - Meer checks voor fouten, zie suggesties functies                   |
# |----------------------------------------------------------------------------|
class JsonBase:
    def __init__(self):
        self.__teams = dict()
        self.__map = {"vertices": [[1, {"origin": 3, "straight": 2}],[2, {"origin": 1, "straight": 3}],[3, {"origin": 2, "straight": 1, "left": 4}],
        [4, {"origin": 3, "straight": 1, "left": 2}]],"edges": [[1, 2, 0.3],[1, 3, 0.5],[3, 1, 0.5],[2, 3, 0.1],[3, 2, 0.1],[3, 4, 0.7],[4, 2, 0.3],[4, 1, 0.8]]}
        self.__parcels = {"available-parcels": [[142, 1, 2],[145, 2, 3],[147, 2, 1], [148, 1, 2], [149, 1, 2], [152, 1, 2], [162, 1, 2], [172, 1, 2]],"on-the-road-parcels": [],"delivered-parcels": []}
        self.__positions = {"positions":[]}
        self.__secret_key = 'SecretKey'
    def get_map(self):
        return json.dumps(self.__map)
    def get_parcels(self):
        return json.dumps(self.__parcels)
    def get_positions(self):
        return json.dumps(self.__positions)
    # Parcels zijn valid als het uit een lijst van lijsten met lengte 3 bestaat, de inhoud van deze laatste lijsten moet een int zijn
    # Eg; [[parcelnb,from,end],[parcelnb2,from2,end2]]
    # TODO: check if parcelnumber, from en end valid zijn
    def is_valid_parcels(self,parcels):
        if isinstance(parcels,list):
            result = True
            for parcel in parcels:
                if isinstance(parcel,list) and len(parcel)==3:
                    for i in parcel:
                        if not isinstance(i,int):
                            result = False
                else:
                    result = False
            return result
        else:
            return False
    def add_parcels(self,key,parcels):
        # TODO: check if there is not already a parcel with the given parcel number, and if the from en end node valid zijn
        if (self.__secret_key == key):
            if self.is_valid_parcels(parcels):
                for parcel in parcels:
                    self.__parcels["available-parcels"].append(parcel)
                return True
            else:
                return False
        else:
            return False
    def check_key(self,team,secretkey):
        if not secretkey:
            return False

        else:
            key = self.__teams.get(team,False)
            print 'Check key',key
            if not key:
                return False
            return (secretkey == key)
        return False
    # If a team has already a key it will be overwritten
    # The key may not be False
    def add_team(self,team,key):
        if not key:
            return False
        else:
            self.__teams[team]= key
            return True

    def delete_team(self,team,key):
        try:
            if not self.check_key(team,key):
                return False
            del self.__teams[team]
            return True
        except:
            return False
    def claimmer(self,parcel_nb,team,key):
        ## TODO CHECK if the team has already a parcel
        if not self.check_key(team,key):
            return False
        available = self.__parcels["available-parcels"]
        for i in range(len(available)):
            if available[i][0] == parcel_nb:
                t = available[i]
                t.append(team)
                self.__parcels["on-the-road-parcels"].append(t)
                del self.__parcels["available-parcels"][i]
                return True
        return False
    def deliver(self,parcel_nb,team,key):
        if not self.check_key(team,key):
            return False
        ontheroute = self.__parcels["on-the-road-parcels"]
        for i in range(len(ontheroute)):
            if (ontheroute[i][0] == parcel_nb) and (ontheroute[i][-1] == team):
                print 'OK'
                t = ontheroute[i]
                del self.__parcels["on-the-road-parcels"][i]
                self.__parcels["delivered-parcels"].append(t)
                return True
        return False
    def update_position(self,from_node,end_node,team,key):
        # TODO: check if from en end node valid zijn
        if not self.check_key(team,key):
            return False
        positions = self.__positions["positions"]
        for i in range(len(positions)):
            if positions[i][0] == team:
                del positions[i]

        self.__positions["positions"].append([team,from_node,end_node ])
        return True
