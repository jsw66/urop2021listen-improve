from flask import Flask, redirect, url_for, render_template, request, flash, json, session
from flask.wrappers import Response
from scraper2 import*
from forms import RegistrationForm, LoginForm
from forms import*
from datetime import datetime, timedelta
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
import csv
import os.path

app = Flask(__name__)
app.config['SECRET_KEY'] = '427fc9fe78101d55040ef9cfa0742b0b'
app.permanent_session_lifetime = timedelta(days=1)
bcrypt = Bcrypt(app)

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

        df = pd.read_csv("users.csv")
        existing_usernames = df["username"]
        username_list = [name for name in existing_usernames]

        if username in username_list:
            return redirect(url_for('register'))

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

        
        #change this directory to the cwd
        #appends user info to the entire user csv file
        with open("C://Users//josep//urop//users.csv", "a", newline='') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            wr.writerow([username, hashed_password, str(age), native_lang, native_freq, second_lang, second_time, second_freq, third_lang, third_time, third_freq, impairments])

        #creates a user specific csv where question id and answers can be stored
        if os.path.isfile(f"C://Users//josep//urop//{username}_answers.csv"):
            print(f"username: {username} answersheet already exists")
        else:
            col_vals = ["question_id", "answer"]
            df = pd.DataFrame(columns = col_vals)
            df.to_csv(f'{username}_answers.csv', mode='a', header=True)
            print(f"username: {username} answersheet has been created")

        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form, posts=lang_list)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        #checks username and hashed password
        df = pd.read_csv("users.csv")

        entered_username = request.form.get("username")
        entered_pw = request.form.get("password")

        existing_usernames = df["username"]
        encrypted_pw_list = df["hashed_password"]

        n = df.index[df.username == entered_username][0]

        correct_pw_encrypted = df["hashed_password"][n]

        if bcrypt.check_password_hash(correct_pw_encrypted, entered_pw):
            #makes closing the browser not forget the logged in user
            session.permanent = True
            session["username"] = entered_username
            return redirect(url_for("home"))
        else:
            flash("incorrect login")
            return redirect(url_for("login"))

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
        return render_template("c1.html", title = "C1", posts=c1_js, username=username)
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug = True)