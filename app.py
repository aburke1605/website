import requests
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    ip = request.remote_addr
    resp = requests.get(f"https://ipinfo.io/{ip}/json")
    data = resp.json()

    country = data.get("country")
    city = data.get("city")
    region = data.get("region")
    return render_template("index.html", country=country, city=city, region=region)

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
