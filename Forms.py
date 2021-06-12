
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Usernameform(FlaskForm):
    username = StringField('Enter your username', validators=[DataRequired()])
    submit = SubmitField('submit')


class SearchPage(FlaskForm):
  search = StringField('Jump to page', [DataRequired()])
  submit = SubmitField('Search')

