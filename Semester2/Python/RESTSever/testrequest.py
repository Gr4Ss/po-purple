import requests

r = requests.post('http://localhost:8080/robots/Paars',data={'key':'245432FDSFQSG'})
print r.text
r = requests.get('http://localhost:8080/map')
print r.json()
