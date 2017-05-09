# Imports required
from pymongo import MongoClient

# Initialize
client = MongoClient('mongodb://tmega:ucsdece188!@tmega-shard-00-00-kcfpq.mongodb.net:27017,tmega-shard-00-01-kcfpq.mongodb.net:27017,tmega-shard-00-02-kcfpq.mongodb.net:27017/user_info?ssl=true&replicaSet=tmega-shard-0&authSource=admin')
db_website = client.website

# Get button value, iterate, then post (change user to your account)
temp_dict = db_website.usrname.find_one({'username':'jwebb'},{'button_three': ()})
new_value = int(temp_dict['button_three']) + 1
db_website.usrname.update({'username': 'jwebb'}, {'$set': {'button_three': new_value}}, upsert=False)
