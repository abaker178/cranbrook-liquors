# Import Dependencies
from flask import Flask, render_template, jsonify, request, redirect
import requests
from datetime import datetime as dt
import os
from flask_sqlalchemy import SQLAlchemy
from models import *
from config import uri # (for testing)

# Create Flask app
app = Flask(__name__)

# Config app for use with Heroku PostgreSQL DB
db_uri = os.environ.get('DATABASE_URL', '').replace("://", "ql://", 1) or uri # (for testing)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# api_route = "http://cranbrook-liquors.herokuapp.com/api"
api_route = "http://127.0.0.1:5000/api" # (for testing)

# Capture creators from models.py
Special = create_special(db)
Staff = create_staff(db)

# Capture specials parameters
query_params = {
    "beer": [Special.id, Special.brand, Special.product, Special.volAmt, Special.volUnit, Special.price, Special.xpack, Special.container],
    "wine": [Special.id, Special.brand, Special.product, Special.volAmt, Special.volUnit, Special.price, Special.varietals, Special.container],
    "spirit": [Special.id, Special.brand, Special.product, Special.volAmt, Special.volUnit, Special.price]
}

now = dt.now()

def format_num(n):
    return n

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
            special = Special(
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
            special = Special(
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
            special = Special(
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

# Edit Special
@app.route("/edit-special")
def edit_special():
    id = request.args.get("id")
    for category in query_params.keys():
        item = db.session.query(*query_params[category]).filter_by(id=id).all()
    return render_template("edit-special.html", item=item)


# Staff page
@app.route("/staff")
def staff():
    staff = db.session.query(Staff).all()
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
    results = db.session.query(*query_params[category]).filter_by(month=query_month, category=category).all()

    if category == "beer":
        data = [{
            "id": result[0],
            "brand": result[1],
            "product": result[2],
            "volume": f"{format_num(result[3])}{result[4]}",
            "price": result[5],
            "xpack": result[6],
            "container": result[7]
        } for result in results]

    elif category == "wine":
        data = [{
            "id": result[0],
            "brand": result[1],
            "product": result[2],
            "volume": f"{format_num(result[3])}{result[4]}",
            "price": result[5],
            "varietals": result[6],
            "container": result[7]
        } for result in results]

    else:
        data = [{
            "id": result[0],
            "brand": result[1],
            "product": result[2],
            "volume": f"{format_num(result[3])}{result[4]}",
            "price": result[5],
        } for result in results]

    return jsonify(data)

####################
#### END ROUTES ####
####################


# Run app if running from main
if __name__ == "__main__":
    app.run(debug=True)