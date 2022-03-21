from curses import REPORT_MOUSE_POSITION
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
# use flask pymongo to set the connection to the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsData"
mongo = PyMongo(app)

@app.route("/")
def index():
    # acces the info from database
    marsData = mongo.db.marsData.find_one()
    
    return render_template("index.html", mars=marsData)
    

@app.route("/scrape")
def scrape():
    # to a database collection (table)
    marsTable = mongo.db.marsData

    # drop the table if exists 
    mongo.db.marsData.drop()

    # scrape mars script
    mars_data = scrape_mars.scrape_all()

    # take the dictionary and load it to MongoDB
    marsTable.insert_one(mars_data)

    # go back to the index route
    return redirect("/")

if __name__ == "__main__":
    app.run()
