def claimmer(parcels,parcel_nb,team):
    available = parcels["available-parcels"]
    for i in range(len(available)):
        if available[i][0] == parcel_nb:
            del parcels["available-parcels"][i]
            t = available[i]
            t.append(team)
            parcels["on-the-road-parcels"].append(t)
            return True
    return False
def check_key(teams,team,secretkey):
    key = teams.get(team,False)
    return (secretkey == key)
