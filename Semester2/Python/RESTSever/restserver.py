from bottle import Bottle,run,request,post,get,delete,put
import json
import helper
app = Bottle()
DEBUG = True
TEAMS = dict()
MAP = json.dumps({"vertices": [[1, {"origin": 3, "straight": 2}],[2, {"origin": 1, "straight": 3}],[3, {"origin": 2, "straight": 1, "left": 4}],[4, {"origin": 3, "straight": 1, "left": 2}]],"edges": [[1, 2, 0.3],[1, 3, 0.5],[3, 1, 0.5],[2, 3, 0.1],[3, 2, 0.1],[3, 4, 0.7],[4, 2, 0.3],[4, 1, 0.8]]})
PARCELS = {"available-parcels": [[142, 1, 2],[145, 2, 3],[147, 2, 1]],"on-the-road-parcels": [],"delivered-parcels": []}
@app.post('/robots/<team>')
def register(team):
    global TEAMS,DEBUG
    try:
        value = request.forms.get('key',False)
        if not value:
            return 'SORRY'
        TEAMS[team] = value
        if DEBUG:
            print TEAMS
        return 'OK'
    except:
        return 'SORRY'

@app.delete('/robots/<team>/<secretkey>')
def delete(team,secretkey):
    global TEAMS,DEBUG
    try:
        result = helper.check_key(TEAMS,team,secretkey)
        if not result:
            return 'SORRY'
        del TEAMS[team]
        if DEBUG:
            print TEAMS
    except:
        return 'SORRY'
@app.get('/map')
def return_map():
    global MAP
    return MAP
@app.get('/parcels')
def return_parcels():
    global PARCELS
    return json.dumps(PARCELS)
@app.put('/robots/<team>/claim/<parcel_nb>')
def claim_parcel(team,parcel_nb):
    global PARCELS,TEAMS
    try:
        value = request.forms.get('key',False)
        result = helper.check_key(TEAMS,team,value)
        if not result:
            return 'SORRY'
        ok = helper.claimmer(PARCELS,parcel_nb,team)
        if DEBUG:
            print PARCELS
        return  'OK' if ok else 'SORRY'
    except:
        return 'SORRY'



app.run(host='localhost',port='8080',debug=True)
