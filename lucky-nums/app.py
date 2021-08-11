from flask import Flask, render_template, jsonify, request
import requests
from random import randint
from forms import LuckyNumForm


app = Flask(__name__)
num = randint(1, 100)

def get_fact_for_num(num, type="trivia"):

    resp = requests.get(f"http://numbersapi.com/{num}/{type}")
    return resp.text



@app.route("/api/get-lucky-num", methods=["POST"])
def get_lucky_num():
    
    r = request.json

    form = LuckyNumForm(csrf_enabled=False, data=r)

    if form.validate_on_submit():
        num = randint(1, 100)
        year = r['year']

    #return jsonify(num={"hello": "world"})
        return jsonify(
            num={"num": num,
                "fact": get_fact_for_num(num)},
            year={"year": year,
                "fact": get_fact_for_num(year, type="year")},
        )
    else:
        return jsonify(errors=form.errors)
    
@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")