from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient
from flask_table import Table, Col

app = Flask(__name__, static_path="/static")

client = MongoClient('mongodb://tmega:ucsdece188!@tmega-shard-00-00-kcfpq.mongodb.net:27017,tmega-shard-00-01-kcfpq.mongodb.net:27017,tmega-shard-00-02-kcfpq.mongodb.net:27017/user_info?ssl=true&replicaSet=tmega-shard-0&authSource=admin')
db_website = client.website
# db_website.trabbani.insert_one({"username":"trabbani","shape":"square", "button_one": "1", "button_two": "1", "button_three": "-", "button_four": "1"})
# db_website.cmarshall.insert_one({"username":"cmarshall","shape":"-", "button_one": "-", "button_two": "-", "button_three": "-", "button_four": "-"})
# db_website.dren.insert_one({"username":"dren","shape":"-", "button_one": "-", "button_two": "-", "button_three": "-", "button_four": "-"})
# db_website.nstein.insert_one({"username":"nstein","shape":"-", "button_one": "-", "button_two": "-", "button_three": "-", "button_four": "-"})


class ItemTable(Table):
    name = Col('Username   ')
    shape = Col('Shape   ')
    button_one = Col('Button_One   ')
    button_two = Col('Button_Two   ')
    button_three = Col('Button_Three   ')
    button_four = Col('Button_Four   ')


class Item(object):
    def __init__(self, name, shape, button_one, button_two, button_three, button_four):
        self.name = name
        self.shape = shape
        self.button_one = button_one
        self.button_two = button_two
        self.button_three = button_three
        self.button_four = button_four


@app.route('/')
def index():
    db_website.trabbani.insert_one({"username":"trabbani","shape":"square", "button_one": "-", "button_two": "-", "button_three": "-", "button_four": "1"})
    return render_template('home.html')

@app.route('/sign_up/successful/', methods = ['POST', 'GET'])
def sign_up():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['pass']
    referl = request.form['referl']
    uname = fname[0] + lname
    usrname = uname.lower()
    test = bool(db_website.user_info.find_one({'username':usrname, 'password':password}))
    if test:
        return render_template("unsuccessful_sign_in.html", username=usrname)
    else:
        db_website.user_info.insert_one({'first_name':fname,'last_name': lname, 'email':email, 'password': password , 'referl':referl, "username": usrname})
        db_website.usrname.insert_one({"username":usrname,"shape":"-", "button_one": "-", "button_two": "-", "button_three": "-", "button_four": "-"})
    #db_website.dashboard_API.find_one({'uname': cmarshall})
    return render_template('sign_up.html', username=fname)

@app.route('/login/successful/',  methods = ['POST', 'GET'])
def login():
    #return render_template("login.html")
    usrname = request.form['uname']
    password = request.form['psw']
    return login_usr(usrname, password)

@app.route('/login/<usrname>/')
def login_usr(usrname, password):
    test = bool(db_website.user_info.find_one({"username":usrname, "password":password}))
    if test:
        #data = db_website.usrname.find_one()
        info_list = []
        temp_list = []

        user = db_website.usrname
        for post in user.find():
            info_list.append(Item(post['username'], post['shape'], post['button_one'], post['button_two'], post['button_three'], post['button_four']))

            table = ItemTable(info_list)
        return render_template("login.html", username=usrname, datab=table)
    else:
        return render_template('unsuccessful_login.html',username=usrname)

if __name__=="__main__":
    app.run()






#Notes:

# for data in db_website.user_info.find(): #iterate through entire database
#     print data
#     print "\n"
# result = db_website.user_info.delete_many({}) #delete entire database
# print result
