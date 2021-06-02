from flask import Flask, render_template, jsonify, request
from datetime import datetime as dt
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/")
def home():
    return jsonify(db)

@app.route("/specials")
def specials():    
    month = dt.now().strftime("%B")
    coll = dt.now().strftime("%b%Y").lower()
    beer = db[coll].find({"category": "beer"})
    wine = db[coll].find({"category": "wine"})
    spirit = db[coll].find({"category": "spirit"})
    return render_template("specials.html", month=month, beer=beer, wine=wine, spirit=spirit)

@app.route("/staff")
def staff():

    today = dt.today()
    staff = db["staff"].find()
    return render_template("staff.html", staff=staff, today=today)

if __name__ == "__main__":
    app.run()