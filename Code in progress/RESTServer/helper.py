import json
# |----------------------------------------------------------------------------|
# |TODO:  - Documentatie                                                       |
# |       - Meer checks voor fouten, zie suggesties functies                   |
# |----------------------------------------------------------------------------|
class JsonBase:
    def __init__(self):
        self.__teams = dict()
        self.__map = {
	"vertices":
	[
		[ 1, {"origin":  5, "left":  10, "right":     2                }],
		[ 2, {"origin":  6, "left":   1, "right":     3, "straight": 12}],
		[ 3, {"origin":  7, "left":   2, "right":     4                }],
		[ 4, {"origin":  7, "left":   3, "right":    11, "straight": 14}],
		[ 5, {"origin":  8, "right":  6, "straight":  1                }],
		[ 6, {"origin":  9, "left":   5, "right":     7, "straight":  2}],
		[ 7, {"origin":  9, "left":   6, "right":     4, "straight":  3}],
		[ 8, {"origin": 10, "right":  9, "straight":  5                }],
		[ 9, {"origin": 11, "left":   8, "right":     7, "straight":  6}],
		[10, {"origin":  8, "left":  11, "right":     1                }],
		[11, {"origin":  9, "left":   4, "right":    10                }],
		[12, {"origin":  2, "right": 13, "straight": 15                }],
		[13, {"origin": 15, "left":  14, "right":    12                }],
		[14, {"origin":  4, "left":  13, "straight": 15                }],
		[15, {"origin": 13, "left":  12, "right":    14                }]
	],
	"edges":
	[
		[ 1,  2,  70.0],
		[ 1,  5,  70.0],
		[ 1, 10, 200.0],
		[ 2,  3,  70.0],
		[ 2,  6,  70.0],
		[ 2, 12, 197.0],
		[ 3,  2,  70.0],
		[ 3,  7,  70.0],
		[ 4,  3,  70.0],
		[ 4,  7, 115.0],
		[ 4, 11, 500.0],
		[ 4, 14, 197.0],
		[ 5,  1,  70.0],
		[ 5,  6,  70.0],
		[ 5,  8,  70.0],
		[ 6,  2,  70.0],
		[ 6,  5,  70.0],
		[ 6,  7,  70.0],
		[ 7,  3,  70.0],
		[ 7,  4, 115.0],
		[ 7,  6,  70.0],
		[ 7,  9, 115.0],
		[ 8,  5,  70.0],
		[ 8,  9,  70.0],
		[ 9,  6,  70.0],
		[ 9,  7, 115.0],
		[ 9,  8,  70.0],
		[10,  1, 200.0],
		[10,  8,  70.0],
		[10, 11,  70.0],
		[11,  4, 500.0],
		[11,  9,  70.0],
		[11, 10,  70.0],
		[12,  2, 197.0],
		[12, 13,  70.0],
		[12, 15, 140.0],
		[13, 12,  70.0],
		[13, 14,  70.0],
		[14,  4, 197.0],
		[14, 13,  70.0],
		[14, 15, 115.0],
		[15, 12, 140.0],
		[15, 13,  70.0],
		[15, 14, 115.0]
	]
}
        self.__parcels = {"available-parcels": [[142, 1, 2],[145, 2, 3],[147, 2, 1], [148, 4, 3], [149, 8, 1], [152, 8, 1], [162, 5, 3], [172, 7, 8]],"on-the-road-parcels": [],"delivered-parcels": []}
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
        for i in range(len(positions)-1,-1,-1):
            if str(positions[i][0]) == team:
                del positions[i]

        self.__positions["positions"].append([team,from_node,end_node ])
        return True
