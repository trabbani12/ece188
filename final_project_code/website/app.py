from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__, static_path="/static")

client = MongoClient('mongodb://tmega:ucsdece188!@tmega-shard-00-00-kcfpq.mongodb.net:27017,tmega-shard-00-01-kcfpq.mongodb.net:27017,tmega-shard-00-02-kcfpq.mongodb.net:27017/user_info?ssl=true&replicaSet=tmega-shard-0&authSource=admin')
db = client.tmega

#temp = db.user_info.find_one() #it's a dictionary
@app.route('/')
def index():
    #db.user_info.insert_one({'username':'Admin', 'password':'password', 'email':'admin@test.edu', 'newsletters':'y'}) ---this would be syntax for adding info to DB
    return render_template('home.html')

if __name__=="__main__":
    app.run()
