from flask import Flask, render_template
from flask_pymongo import PyMongo
from datetime import datetime as dt

app = Flask(__name__)

@app.route("/")
def home():
    app.config["MONGO_URI"] = f"mongodb+srv://website:v2ZdmFKbXTW5uRw@cranbrook.afp5d.mongodb.net/specials?retryWrites=true&w=majority"
    mongo = PyMongo(app)
    
    month = dt.now().strftime("%B")
    coll = dt.now().strftime("%b%Y").lower()
    beer = mongo.db[coll].find({"category": "beer"})
    wine = mongo.db[coll].find({"category": "wine"})
    spirit = mongo.db[coll].find({"category": "spirit"})
    return render_template("specials.html", month=month, beer=beer, wine=wine, spirit=spirit)

@app.route("/staff")
def staff():
    app.config["MONGO_URI"] = f"mongodb+srv://website:v2ZdmFKbXTW5uRw@cranbrook.afp5d.mongodb.net/staffDB?retryWrites=true&w=majority"
    mongo = PyMongo(app)

    today = dt.today()
    staff = mongo.db["staff"].find()
    return render_template("staff.html", staff=staff, today=today)

if __name__ == "__main__":
    app.run(debug=True)