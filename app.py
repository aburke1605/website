import requests
from flask import Flask, request, render_template, send_from_directory

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

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)


@app.route("/")
def index():
    ip = get_client_ip()
    location = geo_lookup(ip)

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
