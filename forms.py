import pandas as pd
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError

x = pd.read_csv("C://Users//josep//urop//Languages.csv", encoding='latin-1')
lang_list = []
for elem in x['Language']:
    lang_list.append(elem)

years = ["1","2","3","4","5","6","7","8","9","10+"]

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                    validators = [DataRequired(), 
                    Length(min = 2, max = 15)])

    age = IntegerField('Age (in years e.g. 18)', validators = [DataRequired()])
                        
    password = PasswordField('Password', validators = [DataRequired()])

    confirm_password = PasswordField('Confirm Password', 
                    validators = [DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', 
                    validators = [DataRequired(), 
                    Length(min = 2, max = 15)])
    
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember login')
    submit = SubmitField('Login')