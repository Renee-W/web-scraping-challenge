import numpy as np
from flask import Flask, jsonify, render_template, redirect

import datetime as dt
from flask_pymongo import PyMongo
import scrape_mars

#################################################
# Database Setup
#################################################

app = Flask(__name__)

# setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
client=PyMongo(app)

@app.route("/")
def home():

    data=client.db.scrape.find_one()
    return render_template("index.html", mars=data)

@app.route("/scrape")
def scraper():
    results=scrape_mars.scrape_all()
    client.db.scrape.update({},results, upsert=True)
    return redirect ("/", code=302)

if __name__ =="__main__":
    app.run(debug=True)
    