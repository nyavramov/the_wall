from flask import Flask, request, render_template
from flask_rq2 import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from json import dumps
import time
import pymongo

app = Flask(__name__)
app.config['RQ_REDIS_URL'] = 'redis://localhost:6379/0'
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

rq = RQ(app)
mongo = PyMongo(app)

# Create the client
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Use the client to create the database
database = client["wall_database"]

# Access a collection in the database
# A collection in MongoDB is the same as a table in SQL databases
collection = database["wall_messages"]

# Get the content of the post request as JSON then access the message
@app.route('/insert', methods=['POST'])
def insert():
    try:
        json_data = request.get_json()
        message = json_data['user_message']
        mongodb_data = { "message" : message }
        insert_message = collection.insert_one(mongodb_data)
        response = dumps({'success' : True}), 200, {'ContentType':'application/json'}
    except Exception as e:
        print("Encountered exception: ", e)
        response = dumps({'success' : False}), 404, {'ContentType':'application/json'}

    return response

# Retrieve all the information from our collection
def get_all_messages():
    all_info = []

    for item in collection.find():
        all_info.append(item["message"])

    return all_info

@app.route('/', methods=['GET'])
def index():
    messages = get_all_messages() 
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run('localhost', debug=True)