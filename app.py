from flask import Flask, render_template
from datetime import datetime as dt

app = Flask(__name__)

@app.route("/")
def home():
    month = dt.now().strftime("%B")
    return render_template("index.html", month=month)

if __name__ == "__main__":
    app.run(debug=True)