from bottle import Bottle,run,static_file, request,post
app = Bottle()

@app.route('/')
def home():
    html = open('website.html','r')
    value = request.query.get('straight',False)
    if value:
        return value
    return html
@app.post('/')
def test_post():
     value = request.forms.get('straight')
     return 'Pieter is cool. Maar Kristof is cooler!', value
@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename,root='/home/pieter/Documenten/Ku Leuven/PenO/po-purple/Semester2/Python/Server')

app.run(host='localhost',port='8080',debug=True)
