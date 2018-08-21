from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from flask import Flask

import models

def name_exists(form, field):
    if models.User.select().where(models.User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')

class EntryForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    date = DateField("Date", validators=[DataRequired()], format='%Y-%m-%d')
    time_spent = IntegerField("Time Spent", validators=[DataRequired()])
    learnings = TextAreaField("What I Learned", validators=[DataRequired()])
    rememberings = TextAreaField("Resources To Remember", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),name_exists])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=2),
                                         EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password',validators=[DataRequired()])
    is_admin = RadioField("Is administrator?", default=False, choices=[("True", True), ("False",False)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


app = Flask(__name__)
app.secret_key = 'asdf9fs82rnu478200fofj01sksal013rbdabcvbgem2'
with app.test_request_context():
    e = EntryForm()
    print(e)
    print(e.title)
    print(e.title.data)
    print(e.title.label)
    print(e.title.id)
    print(e.title.type)
    print(e.title.object_data)
    print(e.date)
    print(e.learnings)
    e.learnings.data="test"
    print(e.learnings.data)
