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
    "beer": [Special.id, Special.brand, Special.product, Special.volAmt, Special.volUnit, Special.price, Special.month, Special.xpack, Special.container],
    "wine": [Special.id, Special.brand, Special.product, Special.volAmt, Special.volUnit, Special.price, Special.month, Special.varietals, Special.container],
    "spirit": [Special.id, Special.brand, Special.product, Special.volAmt, Special.volUnit, Special.price, Special.month]
}

now = dt.now()

def format_num(n):
    return (n, int(n))[n%1==0]

def to_dict(category, item_list):
    if category == "beer":
        data = [{
            "id": attr[0],
            "brand": attr[1],
            "product": attr[2],
            "volume": f"{format_num(attr[3])}",
            "unit": attr[4],
            "price": attr[5],
            "month": attr[6],
            "xpack": attr[7],
            "container": attr[8]
        } for attr in item_list]

    elif category == "wine":
        data = [{
            "id": attr[0],
            "brand": attr[1],
            "product": attr[2],
            "volume": f"{format_num(attr[3])}",
            "unit": attr[4],
            "price": attr[5],
            "month": attr[6],
            "varietals": attr[7],
            "container": attr[8]
        } for attr in item_list]

    else:
        data = [{
            "id": attr[0],
            "brand": attr[1],
            "product": attr[2],
            "volume": f"{format_num(attr[3])}",
            "unit": attr[4],
            "price": attr[5],
            "month": attr[6]
        } for attr in item_list]
    
    return data

def generate_special():
    category = request.form["category"]
    special = Special(
        timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        category = category,
        brand = request.form["brand"].title(),
        product = request.form["product"].title(),
        volAmt = request.form["vol-amount"],
        volUnit = request.form["vol-unit"],
        price = request.form["price"],
        month = request.form["month"],
        xpack = request.form["xpack"] if category == "beer" else 0, # for beer
        container = request.form["container"].title() if category != "spirit" else "", # for beer and wine
        varietals = request.form["varietals"] if category == "wine" else "" # for wine
        # image = "stock" if request.form["image"] == "" else request.form["image"]
    )
    return special

####################
###### ROUTES ######
####################


# Specials
@app.route("/")
def specials():
    disp_month = now.strftime("%B")
    beer = requests.get(f"{api_route}?category=beer").json()
    wine = requests.get(f"{api_route}?category=wine").json()
    spirit = requests.get(f"{api_route}?category=spirit").json()
    return render_template("specials.html", month=disp_month, beer=beer, wine=wine, spirit=spirit)

# Create new specials
@app.route("/create-special", methods=["GET", "POST"])
def new_special():
    # When form is submitted
    if request.method == "POST":
       
        # Create special item based on submitted form fields
        special = generate_special()

        # Add new special to the DB
        db.session.add(special)
        db.session.commit()
        return redirect("/create-special", code=302)

    return render_template("new-special.html")

# Edit Special
@app.route("/edit-special", methods=["GET", "POST"])
def edit_special():
    id = request.args.get("id")

    # When form is submitted
    if request.method == "POST":
        updated = generate_special()
        db.session.query(Special).filter_by(id=id)\
            .update({
                Special.category: updated.category,
                Special.brand: updated.brand,
                Special.product: updated.product,
                Special.volAmt: updated.volAmt,
                Special.volUnit: updated.volUnit,
                Special.price: updated.price,
                Special.month: updated.month,
                Special.xpack: updated.xpack,
                Special.container: updated.container,
                Special.varietals: updated.varietals,
                }, synchronize_session= False)
        db.session.commit()
        return redirect(f"/preview?month={request.form['month']}")
    
    item_category = db.session.query(Special.category).filter_by(id=id).all()[0][0]
    item_info = db.session.query(*query_params[item_category]).filter_by(id=id).all()
    item_dict = to_dict(item_category, item_info)[0]

    return render_template("edit-special.html", item=item_dict, category=item_category)


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
    item_dicts = to_dict(category, results)
    return jsonify(item_dicts)

####################
#### END ROUTES ####
####################


# Run app if running from main
if __name__ == "__main__":
    app.run(debug=True)