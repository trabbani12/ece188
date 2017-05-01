from flask import Flask, render_template, redirect, request
from pymongo import MongoClient


app = Flask(__name__, static_path="/static")

client = MongoClient('mongodb://tmega:ucsdece188!@tmega-shard-00-00-kcfpq.mongodb.net:27017,tmega-shard-00-01-kcfpq.mongodb.net:27017,tmega-shard-00-02-kcfpq.mongodb.net:27017/user_info?ssl=true&replicaSet=tmega-shard-0&authSource=admin')
db = client.tmega

#temp = db.user_info.find_one() #it's a dictionary
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/sign_up/successful/', methods = ['POST', 'GET'])
def sign_up():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['pass']
    referl = request.form['referl']
    uname = fname[0] + lname
    db.user_info.insert_one({'first_name':fname,'last_name': lname, 'email':email, 'password': password , 'referl':referl, "username":uname})
    return render_template('sign_up.html', username=fname)

@app.route('/login/successful/',  methods = ['POST', 'GET'])
def login():
    #return render_template("login.html")
    usrname = request.form['uname']
    return login_usr(usrname)

@app.route('/login/<usrname>/')
def login_usr(usrname):
    cursor = collection.find({})
    count = cursor.count()
    print count
    return render_template("login.html", username=usrname)

if __name__=="__main__":
    app.run()






#Notes:

# for data in db.user_info.find(): #iterate through entire database
#     print data
#     print "\n"
# result = db.user_info.delete_many({}) #delete entire database
# print result
