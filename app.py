from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True, port=8080)
