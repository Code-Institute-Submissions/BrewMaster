#!/usr/bin/python3
import os
from flask import Flask
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'brew_master'
app.config["MONGO_URI"] = 'mongodb+srv://root:rootbabyboy@honeycluster.v8y4e.mongodb.net/brew_master?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_log')
def test():
    return 'Testing my flask functioning'
    return render_template("log.html", log=mongo.db.log.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
