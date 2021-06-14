from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from models import *

# Create Flask app
app = Flask(__name__)

# Config app for use with Heroku PostgreSQL DB 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "").replace("://", "ql://", 1).replace('"',"'",1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

Beer = create_beer(db)
Wine = create_wine(db)
Spirit = create_spirit(db)
Staff = create_staff_member(db)



db.session.query(Beer.brand).all()