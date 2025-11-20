from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
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
