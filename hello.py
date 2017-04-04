from flask import Flask, render_template, request, make_response
from random import randint
from time import time
from humbledb import Mongo, Document

app = Flask(__name__)

class Operation(Document):
  config_database = 'Operaciones'
  config_collection = 'sumas'
  v1 = 'op1'
  v2 = 'op2'
  ellapsed = 'ellapsed'
  timestamp = 'timestamp'

  def check(self, v):
    return self.v1 + self.v2 == v

@app.route("/", methods=['GET', 'POST'])
def checkValue():
  if request.method == 'GET':
    op = Operation()
    op.v1 = randint(0, 100)
    op.v2 = randint(0, 100)
    op.ellapsed = 0
    op.timestamp = time()
    return render_template("formSimple.html", vs = op)

  if request.method == 'POST':
    op = Operation()
    result = int(request.form['value'])
    op.v1  = int(request.form['v1'])
    op.v2  = int(request.form['v2'])
    op.ellapsed = time() - float(request.form['timestamp'])
    if (op.check(result)):
      with Mongo:
        Operation.insert(op)
      return render_template("resultSimple.html", value = op)
    else:
      op.timestamp = float(request.form['timestamp'])
      return render_template("formSimple.html", vs = op)

@app.route('/list',methods = ["GET"])
def list():
    with Mongo:
      ops = Operation.find()

      ss = ""
      for o in ops:
        try:
          ss += str(o.v1)
          ss += ";" 
          ss += str(o.v2)
          ss += ";" 
          ss += str(o.ellapsed)
          ss += "\n"
        except Exception as e:
          print e
      print ss
      output = make_response(ss)
      output.headers["Content-Disposition"] = "attachment; filename=export.csv"
      output.headers["Content-type"] = "text/csv"
      return output

if __name__ == "__main__":
    app.run(debug=True)