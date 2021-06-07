# Import Dependencies
from flask import Flask, render_template, jsonify, request, redirect
from datetime import datetime as dt
import os
from flask_sqlalchemy import SQLAlchemy
from models import *

# Create Flask app
app = Flask(__name__)

# Config app for use with Heroku PostgreSQL DB 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Capture specials creators from models.py
Beer = create_beer(db)
Wine = create_wine(db)
Spirit = create_spirit(db)


####################
###### ROUTES ######
####################


# Home
@app.route("/")
def home():
    return "IT'S ALIVE"

# Specials
@app.route("/specials")
def specials():    
    month = dt.now().strftime("%B")
    coll = dt.now().strftime("%b%Y").lower()
    beer = db[coll].find({"category": "beer"})
    wine = db[coll].find({"category": "wine"})
    spirit = db[coll].find({"category": "spirit"})
    return render_template("specials.html", month=month, beer=beer, wine=wine, spirit=spirit)

# Create new specials
@app.route("/post/specials", methods=["GET", "POST"])
def new_special():
    # When form is submitted
    if request.method == "POST":
        # Capture universal fields
        category = request.form["category"]
        brand = request.form["brand"]
        product = request.form["product"]
        volAmt = request.form["volAmt"]
        volUnit = request.form["volUnit"]
        price = request.form["price"]
        image = "stock" if request.form["image"] == "" else request.form["image"]

        # Capture unique fields
        ## BEER
        if category == "beer":
            xpack = request.form["xpack"]
            medium = request.form["medium"]
            special = Beer(
                category=category,
                brand=brand,
                product=product,
                volAmt=volAmt,
                volUnit=volUnit,
                xpack=xpack,
                medium=medium,
                price=price,
                image=image)

        ## WINE
        elif category == "wine":
            varietals = request.form["varietals"]
            medium = request.form["medium"]
            special = Wine(
                category=category,
                brand=brand,
                product=product,
                volAmt=volAmt,
                volUnit=volUnit,
                varietals=varietals,
                medium=medium,
                price=price,
                image=image)
        
        ## SPIRITS
        else:
            special = Spirit(
                category=category,
                brand=brand,
                product=product,
                volAmt=volAmt,
                volUnit=volUnit,
                price=price,
                image=image)
        
        # Add new special to the DB
        db.session.add(special)
        db.session.commit()
        return redirect("/post/specials", code=302)

    return render_template("new-special.html")

# Staff page
@app.route("/staff")
def staff():

    today = dt.today()
    staff = db["staff"].find()
    return render_template("staff.html", staff=staff, today=today)

####################
#### END ROUTES ####
####################


# Run app if running from main
if __name__ == "__main__":
    app.run()