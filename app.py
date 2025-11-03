from flask import Flask, render_template, send_from_directory, request

from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

count = 0
client_ips = []

@app.route("/")
def index():
    global count, client_ips
    client_ip = request.remote_addr
    if client_ip not in client_ips:
        count += 1
        client_ips.append(client_ip)
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

@app.route("/visits")
def visits():
    return f"visits: {count}"

@app.route("/debug")
def debug():
    return dict(request.headers)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
