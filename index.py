from flask import Flask, render_template, make_response
from flask import request
from random import randint
from time import time
import pymongo
import cPickle
from pymongo import MongoClient

MONGODB_URI = "mongodb://heroku_90h5lf7z:ivpvq47r7je2j93993eba59pp6@ds117199.mlab.com:17199/heroku_90h5lf7z"


client = MongoClient(MONGODB_URI)
db = client.get_default_database()
collection = db.add


with open('classifier.pkl', 'rb') as fid:
    regr_loaded = cPickle.load(fid)

app = Flask(__name__)

@app.route('/',methods = ["GET", "POST"])
def hello_world():
  if request.method == 'POST':
    op = {}
    op["result"] = request.form['value']
    op["v1"] = request.form['v1']
    op["v2"] = request.form['v2']
    op["ellapsed"] = str(time() - float(request.form['timestamp']))
    if int(op["v1"]) + int(op["v2"]) == int(op["result"]):
      collection.insert(op)
      op["prediction"] = regr_loaded.predict([int(op["v1"]), int(op["v2"]),  int(op["v1"]) < 10 or int(op["v2"]) < 10, int(op["v1"]) % 10, int(op["v2"]) % 10])[0]
      return render_template("result.html", value = op)
    else:
      op["timestamp"] = float(request.form['timestamp'])
      return render_template("form.html", vs = op)
  if request.method == 'GET':
    values = {}
    values["v1"] = randint(0, 100)
    values["v2"] = randint(0, 100)
    values["timestamp"] = time()
    values["ellapsed"] = 0
    return render_template("form.html", vs = values)

@app.route('/list',methods = ["GET"])
def list():
    ops = collection.find()
    ss = ""
    for o in ops:
      try:
        ss += o["v1"] 
        ss += ";" 
        ss += o["v2"] 
        ss += ";" 
        ss += o["ellapsed"] 
        ss += "\n"
      except Exception as e:
        pass
    output = make_response(ss)
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


if __name__ == "__main__":
  app.run()
