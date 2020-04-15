from flask import Flask, request, url_for, jsonify,redirect, render_template
from flask_pymongo import PyMongo
import requests
import json
import time
from bson import BSON
from bson import json_util
from pymongo import MongoClient
from datetime import datetime
from flask_charts import Chart,GoogleCharts
from matplotlib import pyplot as plt
import numpy




app = Flask (__name__)
app.config['MONGO_URI'] = "mongodb+srv://ShakeebSharief:shakeeb@cluster0-0u0gt.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)
timestamp = ''
client = MongoClient("mongodb+srv://ShakeebSharief:shakeeb@cluster0-0u0gt.mongodb.net/test?retryWrites=true&w=majority")




@app.route('/')

def index():
    return render_template('index.html')

@app.route("/countrylist")

def all():
   
    db = client.currency
    collection = db['currency']
    cursor = collection.find({})
    list1=[]
    for document in cursor:
        final = json.dumps(document, indent=4, default=json_util.default)
        #print(final)
        x=json.loads(final)
        #print(x)
        a= render_template('countrylist.html',x=x)
    
    return a

@app.route("/refresh")
def refresh():
    
    db = client.currency
    while True:
        r = requests.get("http://api.currencylayer.com/live?access_key=9c6752c75ecb1e27412bba3cb6fc5f44")
        if r.status_code == 200:
            data = r.json()
            #print(data)
            db.currency.insert_one(data)
            #time.sleep(60)
            break
        else:
            exit()
    timestamp = datetime.now()
    return redirect('/countrylist')



@app.route("/converter")

def converter():
    
    db = client.currency
    collection = db['currency']
    cursor = collection.find({})
    list1=[]
    for document in cursor:
        final = json.dumps(document, indent=4, default=json_util.default)
        #print(final)
        set1=json.loads(final)
        #print(x)
        a= render_template('converter.html',set1=set1)
    
    return a

@app.route("/result", methods=['POST'])
def result():
    country1 = str(request.form['countries1'])
    country2 = str(request.form['countries2'])
    amount = float(request.form['amount'])
    db = client.currency
    collection = db['currency']
    cursor = collection.find({})
    list1=[]
    for document in cursor:
        final = json.dumps(document, indent=4, default=json_util.default)
        #print(final)
        set1=json.loads(final)
    if(country1 == 'USD' and country2 != 'USD'):
        finalresult = set1["quotes"][country2]*amount
    elif(country1 != 'USD' and country2 == 'USD'):
        finalresult = amount/set1["quotes"][country1]
    else:
        result1 = (amount/set1["quotes"][country1])
        finalresult = (set1["quotes"][country2]*result1)
    b = 'The converted rate of '+str(amount)+' '+country1[-3:]+' is '+str(finalresult)+' '+country2[-3:]
    return render_template("result.html",b = b)


@app.route("/trend")
def trend():
        
    a= render_template('tendt.html')
    
    return a

@app.route("/tresult", methods=['POST'])
def tresult():

    cntry = str(request.form['cntry'])
    db = client.currency
    collection = db['currency']
    cursor = collection.find({})
    dates=[]
    rates=[]
    

    for document in cursor:
        final = json.dumps(document, indent=4, default=json_util.default)
        #print(final)
        x=json.loads(final)
        
        b = datetime.utcfromtimestamp(x["timestamp"]).strftime('%Y-%m-%d')
        dates.append(b)
        
        rates.append(x["quotes"][cntry])
        
    
    while(len(rates)>5):
        del rates[0]
    
    while(len(dates)>5):
        del dates[0]
    #print(x["quotes"])
    
    
    plt.plot(rates)
    plt.xticks(numpy.arange(len(dates)),dates,rotation = 45)

    plt.xlabel('Date')
    plt.ylabel('Rate for 1$')
    plt.title('Currency Trend')
    g= plt.show()
    
    return render_template("tresult.html",g=g)