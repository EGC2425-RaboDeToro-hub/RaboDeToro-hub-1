from flask_wtf import FlaskForm
from wtforms import SubmitField


class EmailForm(FlaskForm):
    submit = SubmitField('Save email')
