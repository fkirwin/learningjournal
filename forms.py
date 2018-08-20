from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Length


class EntryForm(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(min=2)])
    date = DateField("date", validators=[DataRequired()])
    time_spent = IntegerField("time-spent", validators=[DataRequired()])
    learnings = TextAreaField("what - i - learned", validators=[DataRequired()])
    rememberings = TextAreaField("resources - to - remember", validators=[DataRequired()])
