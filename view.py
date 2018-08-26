# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import datetime as dt
import pandas as pd
from model import FareCalculator, FareTable

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # need some improvement
    start = request.form['start']
    start = start.replace('T', '-').replace(':', '-').split('-')
    start = [int(v) for v in start]
    start = dt.datetime(*start)
    end = request.form['end']
    end = end.replace('T', '-').replace(':', '-').split('-')
    end = [int(v) for v in end]
    end = dt.datetime(*end)

    distance = float(request.form['distance'])
    
    calculator = FareCalculator(start, end, distance)
    plans = calculator.fare_table.index
    result = pd.DataFrame(columns=[], index=plans)
    for plan in plans:
        result.at[plan, 'amount'] = calculator.calc_fare(plan)
    
    return ('Plan:' + str(result.amount.idxmin()) 
            + ', Amount: ' + str(result.amount.min())
           )

if __name__ == "__main__":
    app.run(debug=True)
