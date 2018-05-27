from flask import Flask
from database import Database
from flask import render_template,flash,request,redirect,url_for,session
from datetime import datetime
import urllib3, json
import bcrypt

app = Flask(__name__)
app.secret_key='mysecret'


@app.before_first_request
def initizalize_database():
    Database.initialize()



def weather_report(city,state):
    http = urllib3.PoolManager()
    r = http.request('GET',
                     'http://api.wunderground.com/api/f3c442098e60ca9c/conditions/q/' + state + '/' + city + '.json')

    f = json.loads(r.data.decode('utf-8'))
    a = f['current_observation']['observation_location']
    b = f['current_observation']['weather']
    c = f['current_observation']['temperature_string']
    d = f['current_observation']["relative_humidity"]
    e = f['current_observation']["wind_string"]
    g = f['current_observation']["wind_mph"]
    h = f['current_observation']['icon_url']
    weather = [city, state, b, h, c, d, e, str(g)]
    return weather


@app.route('/')
def menu():
    weather=weather_report('SFO','CA')
    return render_template('menu.html',weather=weather)


@app.route('/show')
def show():
    entries=Database.get_records()
    return render_template('show.html',entries=entries)


@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"


@app.route('/login', methods=['POST'])
def login():
    name = str(request.form['username'])
    password = str(request.form['password'])
    print(name,password)
    d = Database.find_record({'name': name})
    print(d)
    if d:
        session['logged_in'] = True
        print('login')
        print(d)
        return loggedin(d)
    else:
        flash('wrong password!')
    return home()

@app.route('/logged_in')
def loggedin(doc):
    print(doc)
    city=doc['city']
    city=''.join(city.split())
    print(city)
    state=doc['state']
    weather=weather_report(city,state)
    return render_template('logged_in.html',doc=doc,weather=weather)

@app.route("/log")
def log():
    session['logged_in'] = False
    #return logged_in()
    return home()


@app.route('/find_one/<doc>')

def find_one(doc):
    return render_template('find_show.html',doc=doc)

@app.route('/show_all')

def show_all():
    doc=Database.get_records()
    return render_template('show_all.html',doc=doc)
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form.get('name')
        d=Database.find_record({'name':name})
        if d is None:

            h=request.form['passwd']
            print(type(h))
            hashpass=bcrypt.hashpw(h.encode('utf-8'),bcrypt.gensalt())
            print(hashpass)



            #password=request.form.get('passwd')
            first = request.form.get('first')
            last = request.form.get('last')
            email=request.form.get('email')
            phone_number=request.form.get('phone_number')
            city=request.form['city']
            state=request.form['state']
            doc={'name':name,
             'password':hashpass,
             'first':first,
             'last':last,
             'email':email,
             'phone_number':phone_number,
             'city':city,
             'state':state,
             'date_time':datetime.now().strftime('Date: %A %Y %m %d Time:%I:%M:%S %r')}
            #print(doc)
            Database.insert_record(doc)
            session['name']=request.form['name']
            return redirect('')
        return 'That username already exists'
    if request.method=='GET':
        return render_template('register.html')

@app.route('/sign_in',  methods=['GET','POST'])
def sign_in():
    if request.method=='POST':
        name = request.form['name']

        print(name)
        existing_name = Database.find_one({'name':name})
        print(existing_name)

        print(existing_name['name'],existing_name['password'])#,str(request.form['password']))
        if existing_name:
            print(existing_name['password'],request.form['password'])
            if existing_name['password']==request.form['password']:
                print('hello')
                session['name'] = request.form['name']
                return redirect('')
        return 'Invalid username/password'
    if request.method=='GET':
        return render_template('find_entry.html')



if __name__ == '__main__':
    app.run(debug = True)