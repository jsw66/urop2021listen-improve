from flask import Flask, redirect, url_for, render_template, request, flash, json
from flask.wrappers import Response
from scraper2 import*
from forms import RegistrationForm, LoginForm
from forms import lang_list

app = Flask(__name__)
app.config['SECRET_KEY'] = '427fc9fe78101d55040ef9cfa0742b0b'

@app.route("/")
def home():
    return render_template("consent.html", title = "Home")

@app.route("/consent/")
def consent():
    return render_template("consent.html", title = "Data T&Cs")

@app.route("/about/")
def about():
    return render_template("about.html", title = "About")

@app.route("/register/", methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Acccount created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form, posts = lang_list)

@app.route("/login/", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'abc@abc.com' and form.password.data == 'abc':
            flash("You're logged in.", 'success')
            return redirect(url_for('home'))
        else:
            flash("Unsuccessful login.", 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/b1/", methods = ["GET", "POST"])
def b1():
    #if request.method == "POST":
    #    answer = request.form.get("answer")
    #    return......
    #form = LoginForm()
    #if form.validate_on_submit() == True:
    #    pass
    #else:
    #    flash("You're not logged in. You cannot start the test without being logged in.", 'danger')
    #    return redirect(url_for('login'))
    return render_template("b1.html", title = "B1", posts = b1_list)

@app.route("/b2/")
def b2():
    #form = LoginForm()
    #if form.validate_on_submit() == True:
    #    pass
    #else:
    #    flash("You're not logged in. You cannot start the test without being logged in.", 'danger')
    #    return redirect(url_for('login'))
    return render_template("b2.html", title = "B2", posts = b2_list)

@app.route("/c1/")
def c1():
    #form = LoginForm()
    #if form.validate_on_submit() == True:
    #    pass
    #else:
    #    flash("You're not logged in. You cannot start the test without being logged in.", 'danger')
    #    return redirect(url_for('login'))
    return render_template("c1.html", title = "C1", posts=b1_js)

@app.route("/quiz/")
def quiz():
    return render_template("webquiz.html")

if __name__ == "__main__":
    app.run(debug = True)