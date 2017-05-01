from flask import Flask, render_template, redirect, request
from pymongo import MongoClient


app = Flask(__name__, static_path="/static")

client = MongoClient('mongodb://tmega:ucsdece188!@tmega-shard-00-00-kcfpq.mongodb.net:27017,tmega-shard-00-01-kcfpq.mongodb.net:27017,tmega-shard-00-02-kcfpq.mongodb.net:27017/user_info?ssl=true&replicaSet=tmega-shard-0&authSource=admin')
db = client.tmega

#temp = db.user_info.find_one() #it's a dictionary
@app.route('/')
def index():

    #db.user_info.insert_one({'username':'Admin', 'password':'password', 'email':'admin@test.edu', 'newsletters':'y'}) ---this would be syntax for adding info to DB
    return render_template('home.html')


# @app.route('/sign-up/sucessful/')
# def sign_up():
#     return render_template('sign_up.html', username="Admin")

@app.route('/sign_up/successful/', methods = ['POST', 'GET'])
def sign_up():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['pass']
    referl = request.form['referl']

    return render_template('sign_up.html', username=fname)

@app.route('/login/successful/',  methods = ['POST', 'GET'])
def login():
    #return render_template("login.html")
    usrname = request.form['uname']
    return login_usr(usrname)

@app.route('/login/<usrname>/')
def login_usr(usrname):
    return render_template("login.html", username=usrname)

# @app.route('/sign-up-sucessful')
# def sign_up():
#     form = cgi.FieldStorage()
#     searchterm =  form.getvalue('searchbox')
#     return render_template('sign_up.html', username="Testing")

if __name__=="__main__":
    app.run()
