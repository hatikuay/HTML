from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    date = datetime.now()
    return render_template("about.html", date=date)


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/products')
def products():
    return render_template("products.html")


@app.route("/greet/<name>")
def greet(name):
    return render_template("greet.html", name=name, length=len(name))


if __name__ == "__main__":
    app.run()
