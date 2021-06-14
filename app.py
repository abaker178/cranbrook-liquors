# Import Dependencies
from flask import Flask, render_template, jsonify, request, redirect
from datetime import datetime as dt
import os
from flask_sqlalchemy import SQLAlchemy
from models import *

# Create Flask app
app = Flask(__name__)

# Config app for use with Heroku PostgreSQL DB 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Capture specials creators from models.py
Beer = create_beer(db)
Wine = create_wine(db)
Spirit = create_spirit(db)
Staff = create_staff(db)


####################
###### ROUTES ######
####################


# Home
@app.route("/")
def home():
    return "<a href='/post/special'>New Special</a> <a href='/specials'>Specials</a>"

# Specials
@app.route("/specials")
def specials():
    month = dt.now().strftime("%Y-%m")
    beer_params = [Beer.brand, Beer.product, Beer.volAmt, Beer.volUnit, Beer.xpack, Beer.container, Beer.price]
    wine_params = [Wine.brand, Wine.product, Wine.volAmt, Wine.volUnit, Wine.varietals, Wine.container, Wine.price]
    spirit_params = [Spirit.brand, Spirit.product, Spirit.volAmt, Spirit.volUnit, Spirit.price]
    beer = db.session.query(*beer_params).filter_by(month=month).all()
    # coll = dt.now().strftime("%b%Y").lower()
    # beer = db[coll].find({"category": "beer"})
    # wine = db[coll].find({"category": "wine"})
    # spirit = db[coll].find({"category": "spirit"})
    return render_template("test.html", db=beer)
        #month=month, beer=beer, wine=wine, spirit=spirit)

# Create new specials
@app.route("/post/special", methods=["GET", "POST"])
def new_special():
    # When form is submitted
    if request.method == "POST":
        # Capture universal fields
        timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        category = request.form["category"]
        brand = request.form["brand"].title()
        product = request.form["product"].title()
        volAmt = request.form["vol-amount"]
        volUnit = request.form["vol-unit"]
        price = request.form["price"]
        month = request.form["month"]
        # image = "stock" if request.form["image"] == "" else request.form["image"]

        # Capture unique fields
        ## BEER
        if category == "beer":
            xpack = request.form["xpack"]
            container = request.form["container"].title()
            special = Beer(
                timestamp=timestamp,
                category=category,
                brand=brand,
                product=product,
                volAmt=volAmt,
                volUnit=volUnit,
                xpack=xpack,
                container=container,
                price=price,
                month=month)
                # image=image

        ## WINE
        elif category == "wine":
            varietals = request.form["varietals"]
            container = request.form["container"].title()
            special = Wine(
                timestamp=timestamp,
                category=category,
                brand=brand,
                product=product,
                volAmt=volAmt,
                volUnit=volUnit,
                varietals=varietals,
                container=container,
                price=price,
                month=month)
                # image=image
        
        ## SPIRITS
        else:
            special = Spirit(
                timestamp=timestamp,
                category=category,
                brand=brand,
                product=product,
                volAmt=volAmt,
                volUnit=volUnit,
                price=price,
                month=month)
                # image=image
        
        # Add new special to the DB
        db.session.add(special)
        db.session.commit()
        return redirect("/post/special", code=302)

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
    app.run(debug=True)