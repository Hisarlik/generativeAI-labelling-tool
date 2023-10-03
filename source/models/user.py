from source.db import db
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(15), unique= True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class LoginForm(FlaskForm):
    username= StringField('username', validators=[InputRequired(), Length(min=5, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=10)])
    remember = BooleanField('Remember me')
class RegisterationForm(FlaskForm):
    email= StringField('Email', validators=[InputRequired(),Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=15)])