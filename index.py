from flask import Flask, render_template
from flask import request
from random import randint

app = Flask(__name__)

@app.route('/',methods = ["GET", "POST"])
def hello_world():
  if request.method == 'POST':
    values = {}
    values["result"] = int(request.form['value'])
    values["v1"] = int(request.form['v1'])
    values["v2"] = int(request.form['v2'])
    return render_template("result.html", value = values)
  if request.method == 'GET':
    values = {}
    values["v1"] = randint(0, 100)
    values["v2"] = randint(0, 100)
    return render_template("form.html", vs = values)

