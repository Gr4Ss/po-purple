import requests


def check_position(positions,team,start,end):
    for pos in postions:
        if pos[0] == team:
            return pos[1] == start and pos[2] == end
    return False

    
# Send key to correct addres
r = requests.post('http://localhost:8080/robots/Paars',data={'key':'245432FDSFQSG'})
assert r.text == 'OK'
# Send key to correct addres
r = requests.post('http://localhost:8080/robots/Orange',data={'key':'Orange'})
assert r.text == 'OK'
# Send an incorrect key
r = requests.post('http://localhost:8080/robots/Rood',data={'key':False})
assert r.text == 'SORRY'
# Send no key
r = requests.post('http://localhost:8080/robots/Indigo')
assert r.text == 'SORRY'
# Request the current map
r = requests.get('http://localhost:8080/map')
print 'MAP:',r.json()
# Request the current parcels
r = requests.get('http://localhost:8080/parcels')
print 'PARCELS:', r.json()
# Add new parcel
r = requests.put('/parcels/add',data={'secretkey':'SecretKey','newParcels':'[[153,3,4]]'})
assert r.text == 'OK'
# Add invalid new parcel
r = requests.put('/parcels/add',data={'secretkey':'SecretKey','newParcels':'[153,3,4]'})
assert r.text == 'SORRY'
# Add invalid new parcel
r = requests.put('/parcels/add',data={'secretkey':'SecretKey','newParcels':'Pieter'})
assert r.text == 'SORRY'
# Claim correctly a parcel
r = requests.put('http://localhost:8080/robots/Paars/claim/153',data={'key':'245432FDSFQSG'})
assert r.text == 'OK'
# Deliver parcel incorrectly, already claimed
r = requests.put('http://localhost:8080/robots/Orange/claim/153',data={'key':'Orange'})
assert r.tex == 'SORRY'
# Claim incorrectly a parcel, wrong key
r = requests.put('http://localhost:8080/robots/Paars/claim/153',data={'key':'245432FDSFQlG'})
assert r.text == 'SORRY'
# Claim incorrectly a parcel, wrong  team
r = requests.put('http://localhost:8080/robots/Rood/claim/153',data={'key':'245432FDSFQSG'})
assert r.text == 'SORRY'
# Claim incorrectly a parcel, non existing parcel number
r = requests.put('http://localhost:8080/robots/Paars/claim/13',data={'key':'245432FDSFQSG'})
assert r.text == 'SORRY'
# Deliver parcel correctly
r = requests.put('http://localhost:8080/robots/Paars/delivered/153',data={'key':'245432FDSFQSG'})
assert r.text == 'OK'
# Deliver parcel incorrectly, wrong team
r = requests.put('http://localhost:8080/robots/Orange/delivered/153',data={'key':'Orange'})
assert r.text == 'SORRY'
# Deliver incorrectly a parcel, wrong key
r = requests.put('http://localhost:8080/robots/Paars/delivered/153',data={'key':'245432FDSFQlG'})
assert r.text == 'SORRY'
# Deliver incorrectly a parcel, wrong parcel number
r = requests.put('http://localhost:8080/robots/Paars/delivered/13',data={'key':'245432FDSFQSG'})
assert r.text == 'SORRY'
# Send correctly position
r = requests.put('http://localhost:8080/positions/Paars/1/3',data={'key':'245432FDSFQSG'})
assert r.text == 'OK'
# Send incorrectly position, wrong key
r = requests.put('http://localhost:8080/positions/Paars/1/3',data={'key':'245432FDDMQSG'})
assert r.text == 'SORRY'
# Send incorrectly position, wrong team
r = requests.put('http://localhost:8080/positions/Rood/1/3',data={'key':'245432FDDMQSG'})
assert r.text == 'SORRY'
r = requests.get('http://localhost:8080/positions')
assert check_position(json.loads(r.json())['positions'],'Paars',1,3)
# Delete correctly
r = requests.delete('http://localhost:8080/robots/Paars/245432FDSFQSG')
assert r.text == 'OK'
# Delete incorrectly, wrong key
r = requests.delete('http://localhost:8080/robots/Orange/Red')
assert r.text == 'SORRY'
# Delete incorrectly, wrong team
r = requests.delete('http://localhost:8080/robots/Red/Red')
assert r.text == 'SORRY'
