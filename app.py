import os
from dotenv import load_dotenv

from flask import Flask, request, render_template, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert

import requests
from datetime import datetime
import pytz
from werkzeug.middleware.proxy_fix import ProxyFix


def get_client_ip():
    return (
        request.headers.get("CF-Connecting-IP")
        or request.headers.get("X-Forwarded-For", "").split(",")[0]
        or request.remote_addr
    )

def geo_lookup(ip):
    r = requests.get(f"https://ipinfo.io/{ip}/json")
    return r.json()

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "None")
DB = SQLAlchemy(app)
Migrate(app, DB)

class VisitorInfo(DB.Model):
    __tablename__ = "visitor_info"
    timestamp = DB.Column(DB.DateTime, primary_key=True)
    ip = DB.Column(DB.String(15))
    region = DB.Column(DB.String(64))
    city = DB.Column(DB.String(64))
    country = DB.Column(DB.String(64))

@app.route("/")
def index():
    data_table = DB.Table("visitor_info", DB.metadata, autoload_with=DB.engine)

    ip = get_client_ip()
    location = geo_lookup(ip)

    query = (
        insert(data_table)
        .values(
	    timestamp=datetime.now(pytz.timezone("NZ")),
            ip=ip,
            region=location.get("region", None),
            city=location.get("city", None),
            country=location.get("country", None),
	)
    )
    DB.session.execute(query)
    DB.session.commit()

    return render_template("index.html")

@app.route("/snake")
def snake():
    return render_template("snake.html")

@app.route("/collider")
def collider():
    return render_template("Collider.html")

@app.route("/Collider.data")
def collider_data():
    return send_from_directory('static', "emscripten/Collider.data")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
