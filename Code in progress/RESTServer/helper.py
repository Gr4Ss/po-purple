import json
# |----------------------------------------------------------------------------|
# |TODO:  - Documentatie                                                       |
# |       - Meer checks voor fouten, zie suggesties functies                   |
# |----------------------------------------------------------------------------|
class JsonBase:
    def __init__(self):
        self.__teams = dict()
        self.__map = {"edges": [[1, 2, 70.0], [1, 5, 70.0], [1, 10, 200.0], [2, 3, 70.0], [2, 6, 70.0], [2, 12, 197.0], [3, 2, 70.0], [3, 7, 70.0], [4, 3, 70.0], [4, 7, 115.0], [4, 11, 500.0], [4, 14, 197.0], [5, 1, 70.0], [5, 6, 70.0], [5, 8, 70.0], [6, 2, 70.0], [6, 5, 70.0], [6, 7, 70.0], [7, 3, 70.0], [7, 4, 115.0], [7, 6, 70.0], [7, 9, 115.0], [8, 5, 70.0], [8, 9, 70.0], [9, 6, 70.0], [9, 7, 115.0], [9, 8, 70.0], [10, 1, 200.0], [10, 8, 70.0], [10, 11, 70.0], [11, 4, 500.0], [11, 9, 70.0], [11, 10, 70.0], [12, 2, 197.0], [12, 13, 70.0], [12, 15, 140.0], [13, 12, 70.0], [13, 14, 70.0], [14, 4, 197.0], [14, 13, 70.0], [14, 15, 115.0], [15, 12, 140.0], [15, 13, 70.0], [15, 14, 115.0]], "vertices": [[1, {"origin": 5, "right": 2, "left": 10}], [2, {"origin": 6, "straight": 12, "right": 3, "left": 1}], [3, {"origin": 7, "right": 4, "left": 2}], [4, {"origin": 7, "straight": 14, "right": 11, "left": 3}], [5, {"origin": 8, "straight": 1, "right": 6}], [6, {"origin": 9, "straight": 2, "right": 7, "left": 5}], [7, {"origin": 9, "straight": 3, "right": 4, "left": 6}], [8, {"origin": 10, "straight": 5, "right": 9}], [9, {"origin": 11, "straight": 6, "right": 7, "left": 8}], [10, {"origin": 8, "right": 1, "left": 11}], [11, {"origin": 9, "right": 10, "left": 4}], [12, {"origin": 2, "straight": 15, "right": 13}], [13, {"origin": 15, "right": 12, "left": 14}], [14, {"origin": 4, "straight": 15, "left": 13}], [15, {"origin": 13, "right": 14, "left": 12}]]}
        self.__parcels = {"delivered-parcels": [], "available-parcels": [[1, 3, 4], [2, 13, 8], [3, 11, 8], [4, 10, 11], [5, 5, 9], [6, 15, 12], [7, 10, 4], [9, 14, 5], [10, 4, 6], [11, 10, 4], [13, 8, 13], [14, 9, 3], [15, 14, 13], [16, 3, 6], [17, 13, 6], [20, 13, 14], [21, 15, 2], [22, 6, 3], [23, 12, 9], [24, 14, 15], [25, 5, 10], [26, 5, 7], [27, 5, 12], [28, 2, 4], [29, 14, 2], [30, 6, 15], [31, 11, 2], [32, 14, 10], [33, 12, 7], [34, 11, 15], [35, 11, 13], [37, 8, 2], [38, 3, 12], [39, 4, 11], [40, 1, 9], [41, 6, 14], [42, 2, 5], [43, 10, 14], [44, 3, 5], [45, 10, 6], [46, 7, 12], [47, 4, 3], [48, 2, 1], [49, 6, 10], [50, 13, 12], [51, 2, 3], [52, 6, 9], [53, 2, 8], [54, 4, 10], [55, 12, 3], [56, 14, 3], [57, 13, 12], [58, 11, 10], [59, 5, 11], [60, 13, 3], [61, 12, 5], [62, 14, 10], [63, 6, 3], [64, 2, 5], [65, 4, 1], [66, 10, 5], [67, 12, 8], [68, 6, 11], [69, 6, 4], [70, 4, 1], [71, 2, 1], [72, 14, 2], [73, 4, 7], [75, 2, 9], [76, 3, 4], [77, 13, 7], [78, 7, 11], [79, 8, 15], [80, 8, 12], [81, 12, 2], [82, 9, 8], [83, 11, 4], [84, 12, 2], [86, 4, 13], [87, 13, 12], [88, 7, 6], [89, 15, 5], [90, 3, 5], [92, 5, 12], [93, 7, 10], [94, 1, 7], [95, 5, 1], [96, 3, 13], [98, 5, 10], [99, 13, 5], [100, 15, 14], [101, 2, 1], [102, 8, 15], [103, 9, 2], [104, 2, 12], [105, 2, 9], [106, 8, 9], [107, 8, 6], [108, 4, 13], [109, 6, 4], [110, 11, 13], [111, 2, 9], [112, 6, 13], [113, 15, 5], [114, 14, 13], [115, 14, 3], [116, 7, 5], [117, 13, 10], [118, 11, 13], [119, 3, 6], [120, 11, 2], [121, 12, 4], [122, 13, 12], [123, 13, 3], [124, 9, 3], [125, 12, 9], [126, 4, 8], [127, 13, 9], [128, 2, 13], [129, 14, 7], [130, 2, 6], [131, 5, 4], [133, 12, 3], [134, 2, 3], [135, 11, 3], [137, 9, 14], [138, 10, 12], [139, 10, 4], [140, 4, 3], [141, 3, 6], [142, 2, 7], [143, 3, 8], [144, 8, 2], [145, 8, 10], [146, 6, 4], [147, 12, 6], [148, 2, 3], [149, 7, 1], [150, 2, 7], [151, 3, 14], [152, 11, 3], [153, 10, 13], [154, 1, 15], [155, 4, 14], [156, 11, 10], [157, 11, 3], [158, 8, 4], [159, 13, 12], [160, 9, 7], [161, 9, 3], [162, 5, 3], [163, 13, 12], [164, 4, 5], [165, 11, 10], [166, 6, 10], [167, 4, 6], [168, 12, 11], [169, 3, 15], [170, 3, 5], [171, 10, 11], [172, 7, 9], [173, 10, 4], [174, 3, 12], [175, 3, 4], [176, 9, 4], [177, 2, 1], [178, 4, 7], [179, 7, 3], [180, 3, 6], [181, 5, 8], [182, 11, 10], [183, 11, 6], [184, 8, 9], [185, 14, 3], [186, 12, 9], [187, 10, 6], [188, 12, 8], [189, 8, 5], [190, 10, 9], [191, 1, 12], [192, 6, 2], [193, 3, 8], [194, 11, 5], [195, 6, 9], [196, 14, 5], [197, 10, 5], [198, 5, 8], [199, 14, 7], [200, 11, 12]], "on-the-road-parcels": []}
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
