import requests
root = 'http://localhost:8080'
r = requests.post(root + '/keys',data={'command':'Pieter'})
print r.text
