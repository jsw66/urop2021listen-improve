from flask import Flask, redirect, url_for, render_template, request, flash, json, session
from flask.wrappers import Response
from scraper2 import*
from forms import RegistrationForm, LoginForm
from forms import*
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '427fc9fe78101d55040ef9cfa0742b0b'
app.permanent_session_lifetime = timedelta(days=1)
bcrypt = Bcrypt(app)

#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(20), unique=True, nullable=False)
#    age = db.Column(db.Integer, unique=False, nullable=False)
#    password = db.Column(db.String(60), nullable=False)
#
#    native_lang = db.Column(db.String(60), nullable=False)
#    native_freq = db.Column(db.String(60), nullable=False)
#
#    second_lang = db.Column(db.String(60), nullable=True)
#    second_time = db.Column(db.String(60), nullable=True)
#    second_freq = db.Column(db.String(60), nullable=True)
#
#    first_lang = db.Column(db.String(60), nullable=True)
#    first_time = db.Column(db.String(60), nullable=True)
#    first_freq = db.Column(db.String(60), nullable=True)
#
#    def __repr__(self):
#        return f"User('{self.username}', '{self.age}', '{self.native_lang}')"

@app.route("/")
def consent():
    return render_template("consent.html", title = "Data T&Cs")

@app.route("/home/")
def home():
    if "username" in session:
        username = session["username"]
        return render_template("home.html", title = "Home", username = username)
    else:
        return redirect(url_for("login"))

@app.route("/about/")
def about():
    if "username" in session:
        username = session["username"]
        return render_template("about.html", title = "About", username=username)
    else:
        return redirect(url_for("login"))

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        username = request.form.get("username")
        age = request.form.get("age")
        password = request.form.get("password")
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        native_lang = request.form.get("native_lang")
        native_freq = request.form.get("native_freq")

        second_lang = request.form.get("second_lang")
        second_time = request.form.get("second_time")
        second_freq = request.form.get("second_freq")

        third_lang = request.form.get("third_lang")
        third_time = request.form.get("third_time")
        third_freq = request.form.get("third_freq")

        impairments = request.form.get("impairments")

        with open(f"C://Users//josep//urop//users.csv", "a") as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            wr.writerow([username, age, hashed_password, native_lang, native_freq, second_lang, second_time, second_freq, third_lang, third_time, third_freq, impairments])
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form, posts=lang_list)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        #makes closing the browser
        session.permanent = True
        username = request.form.get("username")
        session["username"] = username
        return redirect(url_for("home"))
    else:
        if "username" in session:
            return redirect(url_for("home"))
        return render_template('login.html', title='Login', form=form)

@app.route("/logout/")
def logout():
    flash("You have been logged out!", "info")
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/b1/", methods = ["GET", "POST"])
def b1():    
    if "username" in session:
        username = session["username"]
        return render_template("b1.html", title = "B1", posts=b1_js, username=username)
    else:
        return redirect(url_for("login"))

@app.route("/b2/")
def b2():
    if "username" in session:
        username = session["username"]
        return render_template("b2.html", title = "B2", posts=b2_js, username=username)
    else:
        return redirect(url_for("login"))

@app.route("/c1/")
def c1():
    if "username" in session:
        username = session["username"]
        return render_template("c1.html", title = "C1", posts=b1_js, username=username)
    else:
        return redirect(url_for("login"))

@app.route("/quiz/")
def quiz():
    return render_template("webquiz.html")

if __name__ == "__main__":
    app.run(debug = True)