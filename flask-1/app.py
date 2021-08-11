from flask import Flask, session, render_template, redirect, flash, request
from forex_python.converter import CurrencyRates, CurrencyCodes
from flask_debugtoolbar import DebugToolbarExtension
from decimal import *
from helper import currency_converter



app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



debug = DebugToolbarExtension(app)

@app.route("/home")
def conversion_home_pg():
    """shows start of converting"""

    return render_template("home.html")



@app.route("/home/converted", methods=['POST', 'GET'])
def converted():

    has = request.form['convert-start']
    needs = request.form['convert-too']
    amt = request.form['amount']
    
    c = CurrencyCodes()
    symbol = c.get_symbol(needs)
    
    convert = currency_converter(has, needs, amt)
    
    
    valid_msg = convert.valid_currency()
    if valid_msg != 1:
        flash(f'{valid_msg}')
        return redirect('/home')
    else:
        con = convert.shows_result()
        flash(f"The converted result is: {symbol}{con}")
        return redirect('/home')


