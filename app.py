# Import Dependencies
from flask import Flask, render_template, jsonify, request, redirect
import requests
from datetime import datetime as dt
import os
from flask_sqlalchemy import SQLAlchemy
from models import *
# from config import uri # (for testing)

# Create Flask app
app = Flask(__name__)

# Config app for use with Heroku PostgreSQL DB
db_uri = os.environ.get('DATABASE_URL', '').replace("://", "ql://", 1) # or uri # (for testing)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

api_route = "http://cranbrook-liquors.herokuapp.com/api"
# api_route = "http://127.0.0.1:5000/api" # (for testing)

# Capture specials creators from models.py
Beer = create_beer(db)
Wine = create_wine(db)
Spirit = create_spirit(db)
Staff = create_staff(db)

# Capture specials parameters
query_params = {
    "beer": [Beer.brand, Beer.product, Beer.volAmt, Beer.volUnit, Beer.price, Beer.xpack, Beer.container],
    "wine": [Wine.brand, Wine.product, Wine.volAmt, Wine.volUnit, Wine.price, Wine.varietals, Wine.container],
    "spirit": [Spirit.brand, Spirit.product, Spirit.volAmt, Spirit.volUnit, Spirit.price]
}

now = dt.now()

####################
###### ROUTES ######
####################


# Specials
@app.route("/")
def specials():
    disp_month = now.strftime("%B")
    beer = requests.get(f"{api_route}?category=beer").json()
    wine = requests.get(f"{api_route}?category=wine").json()
    spirit = requests.get(f"{api_route}?category=beer").json()
    return render_template("specials.html", month=disp_month, beer=beer, wine=wine, spirit=spirit)

# Create new specials
@app.route("/create-special", methods=["GET", "POST"])
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
        return redirect("/create-special", code=302)

    return render_template("new-special.html")

# Staff page
@app.route("/staff")
def staff():
    staff = Staff.query.all()
    return render_template("staff.html", staff=staff)

# Preview
@app.route("/preview")
def preview():
    query_month = request.args.get("month")
    this_month = now.strftime("%Y-%m")
    if query_month == None:
        return redirect(f"/preview?month={this_month}")
    else:
        disp_month = dt.strptime(query_month, "%Y-%m").strftime("%B")
        beer = requests.get(f"{api_route}?category=beer&month={query_month}").json()
        wine = requests.get(f"{api_route}?category=wine&month={query_month}").json()
        spirit = requests.get(f"{api_route}?category=spirit&month={query_month}").json()
        return render_template("preview.html", month=disp_month, beer=beer, wine=wine, spirit=spirit)

# API route
@app.route("/api")
def api():
    # Get current time info
    month = request.args.get("month")
    category = request.args.get("category")

    query_month = (month, now.strftime("%Y-%m"))[month == None]

    # Query PostgreSQL for this month's specials
    results = db.session.query(*query_params[category]).filter_by(month=query_month).all()

    if category == "beer":
        data = [{
            "brand": result[0],
            "product": result[1],
            "volume": f"{result[2]}{result[3]}",
            "price": result[4],
            "xpack": result[5],
            "container": result[6]
        } for result in results]

    elif category == "wine":
        data = [{
            "brand": result[0],
            "product": result[1],
            "volume": f"{result[2]}{result[3]}",
            "price": result[4],
            "varietals": result[5],
            "container": result[6]
        } for result in results]

    else:
        data = [{
            "brand": result[0],
            "product": result[1],
            "volume": f"{result[2]}{result[3]}",
            "price": result[4],
        } for result in results]

    return jsonify(data)

####################
#### END ROUTES ####
####################


# Run app if running from main
if __name__ == "__main__":
    app.run()