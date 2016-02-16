import requests

r = requests.post('http://localhost:8080/robots/Paars',data={'key':'245432FDSFQSG'})
print r.text
r = requests.get('http://localhost:8080/map')
print r.json()
r = requests.get('http://localhost:8080/parcels')
print r.json()
r = requests.put('http://localhost:8080/robots/Paars/claim/142',data={'key':'245432FDSFQSG'})
print r.text
r = requests.delete('http://localhost:8080/robots/Paars/245432FDSFQSG')
print r.text
