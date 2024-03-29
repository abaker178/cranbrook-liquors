# Import Dependencies
from flask import Flask, render_template, jsonify, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

# All login code was repurposed from https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
from flask_login import login_manager, login_required, LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import requests
from datetime import datetime as dt
import pytz
import os
from models import *
from config import uri # (for testing)

# Create Flask app
app = Flask(__name__)

# Config app for use with Heroku PostgreSQL DB, sending emails, and login
db_uri = os.environ.get("DATABASE_URL", "").replace("://", "ql://", 1) or uri # (for testing)
app.config.update(dict(
    SECRET_KEY = "su9er!s3cre7@p4ssw0r6#Un6373ct4b1e$",
    SQLALCHEMY_DATABASE_URI = db_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = '',
    MAIL_PASSWORD = ''
))

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

db = SQLAlchemy(app)
mail = Mail(app)

api_route = "http://cranbrook-liquors.herokuapp.com/api"

# Capture creators from models.py
Special = create_special(db)
Staff = create_staff(db)
User = create_user(db)

# Capture specials parameters
query_params = {
    "beer": [Special.id, Special.brand, Special.product, Special.volAmt, Special.volUnit, Special.price, Special.month, Special.xpack, Special.container],
    "wine": [Special.id, Special.brand, Special.product, Special.volAmt, Special.volUnit, Special.price, Special.month, Special.varietals, Special.container],
    "spirit": [Special.id, Special.brand, Special.product, Special.volAmt, Special.volUnit, Special.price, Special.month]
}

now = dt.now(pytz.timezone('US/Eastern'))
weekday = now.weekday()

#######################
###### FUNCTIONS ######
#######################

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

#######################
#### END FUNCTIONS ####
#######################


####################
###### ROUTES ######
####################

# Home Page (Specials)
@app.route("/")
def specials():
    disp_month = now.strftime("%B")
    beer = requests.get(f"{api_route}?category=beer").json()
    wine = requests.get(f"{api_route}?category=wine").json()
    spirit = requests.get(f"{api_route}?category=spirit").json()
    return render_template("specials.html", month=disp_month, beer=beer, wine=wine, spirit=spirit, weekday=weekday)

@app.route("/high-end")
def high_end():
    return render_template("high-end.html", weekday=weekday)

# Contact Page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        message = Message(request.args.get("subject"), sender=request.args.get("email"), recipients=['askus@cranbrookliquors.com'])
        message.body = request.args.get("body")
        mail.send(message)
        return redirect("thank-you.html", code=302)

    return render_template("contact.html", weekday=weekday)

# Hours Page
@app.route("/hours-location")
def hours():
    return render_template("hours-loc.html", weekday=weekday)

# Thank You Page
@app.route("/thank-you")
def thanks():
    render_template("thank-you.html", weekday=weekday)

# Staff page
# @app.route("/staff")
# def staff():
#     staff = db.session.query(Staff).all()
#     return render_template("staff.html", staff=staff)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember")

        user = db.session.query(User).filter_by(email=email).first()

        print(generate_password_hash(user.password))

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect("login") # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect("/dashboard")
    
    return render_template("login.html", weekday=weekday)


#### USER ROUTES ####

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return db.session.query(User).get(int(user_id))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# Create New Special
@app.route("/create-special", methods=["GET", "POST"])
@login_required
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

# Preview Specials
@app.route("/preview")
@login_required
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
        return render_template("preview.html", return_month=query_month, month=disp_month, beer=beer, wine=wine, spirit=spirit)

# Edit Special
@app.route("/edit-special", methods=["GET", "POST"])
@login_required
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

# Delete Special
@app.route("/delete-special")
@login_required
def delete_special():
    id = request.args.get("id")
    current_month = request.args.get("month")
    db.session.query(Special).filter_by(id=id).delete(synchronize_session=False)
    db.session.commit()
    return redirect(f"/preview?month={current_month}")

# Chronicle Ad Editor
@app.route("/chronicle")
@login_required
def chronicle():
    query_month = request.args.get("month")
    this_month = now.strftime("%Y-%m")
    if query_month == None:
        return redirect(f"/chronicle?month={this_month}")
    else:
        disp_month = dt.strptime(query_month, "%Y-%m").strftime("%B")
        return render_template("chronicle.html", return_month=query_month, month=disp_month)


#### API ROUTES ####

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