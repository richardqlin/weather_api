from flask import Flask
from database import Database
from flask import render_template,request,redirect,url_for
from datetime import datetime
import urllib3, json
app = Flask(__name__)


@app.before_first_request
def initizalize_database():
    Database.initialize()


@app.route('/')
def menu():


    state = 'CA'
    city = 'Fremont'
    http = urllib3.PoolManager()
    r = http.request('GET',
                     'http://api.wunderground.com/api/f3c442098e60ca9c/conditions/q/' + state + '/' + city + '.json')

    f = json.loads(r.data.decode('utf-8'))
    a = f['current_observation']['observation_location']
    b = f['current_observation']['weather']
    c = f['current_observation']['temperature_string']
    d=f['current_observation']["relative_humidity"]
    e=f['current_observation']["wind_string"]
    g=f['current_observation']["wind_mph"]
    h = f['current_observation']['icon_url']
    print(type(h))

    print(a)
    print(b)
    print(c)
    print(d)
    weather=[city,state,b,h,c,d,e,g]
    print(weather)
    return render_template('menu.html',weather=weather)


@app.route('/show')
def show():
    entries=Database.get_records()
    return render_template('show.html',entries=entries)


@app.route('/find_one/<doc>')

def find_one(doc):
    return render_template('find_show.html',doc=doc)


@app.route('/add', methods=['GET','POST'])
def add_entry():
    if request.method=='POST':
        name=request.form.get('name')

        password=request.form.get('passwd')
        first = request.form.get('first')
        last = request.form.get('last')
        email=request.form.get('email')
        phone_number=request.form.get('phone_number')

        doc={'name':name,
             'password':password,
             'first':first,
             'last':last,
             'email':email,
             'phone_number':phone_number,
             'date_time':datetime.now().strftime('Date: %A %Y %m %d Time:%I:%M:%S %r')}
        Database.insert_record(doc)
        return redirect('')
    if request.method=='GET':
        return render_template('add_entry.html')

@app.route('/sign_in',  methods=['GET','POST'])
def sign_in():
    if request.method=='POST':
        name = request.form.get('name')
        password = request.form.get('passwd')
        doc={'name':name,'password':password}
        d=Database.find_record(doc)
        print(d)
        return redirect(url_for('find_one',doc=doc))
    if request.method=='GET':
        return render_template('find_entry.html')



if __name__ == '__main__':
    app.run(debug = True)