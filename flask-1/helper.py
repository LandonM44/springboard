from forex_python.converter import CurrencyRates, CurrencyCodes
from flask import request, flash
import string
from decimal import *

class currency_converter():
    def __init__(self, has, needs, amt):
        self.needs = needs
        self.has = has
        self.amt= amt


    def shows_result(self):
        """shows result and return home button"""

        has = request.form['convert-start']
        needs = request.form['convert-too']
        amt = request.form['amount']
        


        c = CurrencyRates()
        result = c.convert(has, needs, Decimal(amt))
        converted_amt = round(result, 2)

        return converted_amt

    
    def valid_currency(self):
        """checks to make sure the specified currency is valid"""

        has = request.form['convert-start']
        needs = request.form['convert-too']
        amt = request.form['amount']

        c = CurrencyCodes()


        if len(has) != 3:
            return "Converting From should only be 3 characters long"
        if len(needs) != 3:
            return "Converting Too should only be 3 characters long"
        if amt.isnumeric() == False:
            return "Amount must be a number"
        else:
            return 1
          
        


