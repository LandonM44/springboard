from os import error
from flask import Flask, render_template, jsonify, request
import random

BASE_URL = "http://numbersapi.com/number"

app = Flask(__name__)

BASE_API_URL = "numbersapi.com"
APP_URL = "127.0.0.1:5000/api/"
#r = request.get('numbersapi.com')

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

@app.route("/api/get-lucky-num")
def list_lucky_nums():

    name = request.args.get('name')
    email = request.args.get('email')
    year = int(request.args.get('year'))
    color = request.args.get('color')
    result = jsonify({"success": "good job"})
    #if request.method == "POST":
    if(not name):
        result = jsonify({"ERROR": "must input name field."})
    elif(not email):
        result = jsonify({"ERROR": "must input email field."})
    elif (year < 1900 or year > 2000):
        result = jsonify({"ERROR": "DOB must be between 1900 and 2000."})
    elif(color not in ["blue", "red", "orange", "green"]):
        result = jsonify({"ERROR": "color must be red, green, orange, or blue."})
    #result = jsonify({"NOTANERROR":"color:" + str(request)})
    return result


    #req_form = requests.form
    #form = [form_data for form_data in req_form]
    #return jsonify(form=form)

    #result = request.form.to_dict()
    #data_list = []
    
    #return print(names)
    #new_obj = {
        #"name": "name",
        #"email": "email",
        #"year": "year",
        #"color": "color"
    #}
    #return json.dumps({'name': name, 'email': "email"})
    #return jsonify(request.form)
    #data_list.append(new_obj)
    #return jsonify(data_list)
    #body = ({'name': 'alice',
            #'email': 'asjlksjaldk'})
    #return jsonify(body)
    #body = [serialize(n) for n in ]
    #return jsonify(serialize=body)